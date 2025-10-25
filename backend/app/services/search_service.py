"""
Search service for managing candidate searches
"""
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import uuid

from app.core.finder import (
    LinkedInCandidateFinder,
    SearchCriteria,
    EnrichmentConfig,
    EntityType
)
from app.models.schemas import (
    SearchRequest,
    SearchResponse,
    SearchStatusResponse,
    SearchStatus,
    Candidate,
    CandidateProperties,
    VerificationResult,
    CriteriaResult,
    EnrichmentResult,
    EntityTypeEnum
)
from app.core.config import settings


class SearchService:
    """Service for managing candidate searches"""

    def __init__(self):
        self.finder = LinkedInCandidateFinder(api_key=settings.EXA_API_KEY)
        self.active_searches: Dict[str, Dict] = {}

    def _convert_entity_type(self, entity: EntityTypeEnum) -> EntityType:
        """Convert API entity type to finder entity type"""
        mapping = {
            EntityTypeEnum.PERSON: EntityType.PERSON,
            EntityTypeEnum.COMPANY: EntityType.COMPANY,
            EntityTypeEnum.RESEARCH_PAPER: EntityType.RESEARCH_PAPER,
            EntityTypeEnum.ARTICLE: EntityType.ARTICLE,
        }
        return mapping[entity]

    async def create_search(self, request: SearchRequest) -> SearchResponse:
        """Create a new candidate search"""

        # Generate unique search ID
        search_id = str(uuid.uuid4())

        # Convert request to SearchCriteria
        criteria = SearchCriteria(
            query=request.query,
            count=request.count,
            entity=self._convert_entity_type(request.entity),
            criteria=request.criteria,
            exclude_criteria=request.exclude_criteria
        )

        # Convert enrichments
        enrichments = [
            EnrichmentConfig(description=desc)
            for desc in request.enrichments
        ]

        # Store search metadata
        self.active_searches[search_id] = {
            "status": SearchStatus.PENDING,
            "query": request.query,
            "count": request.count,
            "created_at": datetime.now(),
            "webset_id": None,
            "candidates": []
        }

        # Start search in background
        asyncio.create_task(self._run_search(search_id, criteria, enrichments))

        return SearchResponse(
            search_id=search_id,
            status=SearchStatus.PENDING,
            query=request.query,
            count=request.count,
            created_at=datetime.now()
        )

    async def _run_search(
        self,
        search_id: str,
        criteria: SearchCriteria,
        enrichments: List[EnrichmentConfig]
    ):
        """Run search in background"""
        try:
            # Update status
            self.active_searches[search_id]["status"] = SearchStatus.IN_PROGRESS

            # Create webset
            webset_id = await asyncio.to_thread(
                self.finder.create_candidate_search,
                criteria,
                enrichments
            )

            self.active_searches[search_id]["webset_id"] = webset_id

            # Wait for results
            results = await asyncio.to_thread(
                self.finder.wait_for_results,
                webset_id,
                check_interval=settings.EXA_CHECK_INTERVAL
            )

            # Convert results to candidates
            candidates = self._convert_results_to_candidates(results)

            # Update search with results
            self.active_searches[search_id]["status"] = SearchStatus.COMPLETED
            self.active_searches[search_id]["candidates"] = candidates

        except Exception as e:
            print(f"Search {search_id} failed: {str(e)}")
            self.active_searches[search_id]["status"] = SearchStatus.FAILED
            self.active_searches[search_id]["error"] = str(e)

    def _convert_results_to_candidates(self, results: List[Dict]) -> List[Candidate]:
        """Convert raw results to Candidate models"""
        candidates = []

        for item in results:
            # Extract verification results
            verification = None
            if "verification" in item and item["verification"]:
                criteria_results = [
                    CriteriaResult(
                        description=cr.get("description", ""),
                        passed=cr.get("passed", False),
                        reasoning=cr.get("reasoning", ""),
                        references=cr.get("references", [])
                    )
                    for cr in item["verification"].get("criteria_results", [])
                ]
                verification = VerificationResult(
                    passed=item["verification"].get("passed", False),
                    criteria_results=criteria_results
                )

            # Extract properties
            props = item.get("properties", {})
            properties = CandidateProperties(
                name=props.get("name"),
                current_role=props.get("current_role"),
                current_company=props.get("current_company"),
                location=props.get("location"),
                linkedin_url=props.get("linkedin_url"),
                email=props.get("email"),
                experience_years=props.get("experience_years"),
                skills=props.get("skills", [])
            )

            # Extract enrichments
            enrichments = [
                EnrichmentResult(
                    description=enr.get("description", ""),
                    status=enr.get("status", "unknown"),
                    result=enr.get("result")
                )
                for enr in item.get("enrichments", [])
            ]

            # Calculate AI score (based on verification)
            score = None
            if verification and verification.criteria_results:
                passed_count = sum(1 for cr in verification.criteria_results if cr.passed)
                total_count = len(verification.criteria_results)
                score = (passed_count / total_count) * 100 if total_count > 0 else 0

            candidate = Candidate(
                id=item.get("id", str(uuid.uuid4())),
                url=item.get("url", ""),
                title=item.get("title", ""),
                status=item.get("status", "unknown"),
                verification=verification,
                properties=properties,
                enrichments=enrichments,
                score=score,
                created_at=datetime.now()
            )

            candidates.append(candidate)

        # Sort by score (highest first)
        candidates.sort(key=lambda x: x.score or 0, reverse=True)

        return candidates

    async def get_search_status(self, search_id: str) -> Optional[SearchStatusResponse]:
        """Get status of a search"""
        if search_id not in self.active_searches:
            return None

        search_data = self.active_searches[search_id]

        # Calculate progress
        total_found = len(search_data["candidates"])
        total_requested = search_data["count"]
        progress_percent = (total_found / total_requested * 100) if total_requested > 0 else 0

        return SearchStatusResponse(
            search_id=search_id,
            status=search_data["status"],
            query=search_data["query"],
            total_requested=total_requested,
            total_found=total_found,
            candidates=search_data["candidates"],
            progress_percent=min(progress_percent, 100)
        )

    async def list_all_searches(self) -> List[SearchStatusResponse]:
        """List all searches"""
        searches = []
        for search_id in self.active_searches:
            status = await self.get_search_status(search_id)
            if status:
                searches.append(status)
        return searches

    async def get_candidates(self, search_id: Optional[str] = None) -> List[Candidate]:
        """Get all candidates or candidates from specific search"""
        if search_id:
            search_data = self.active_searches.get(search_id)
            if search_data:
                return search_data.get("candidates", [])
            return []

        # Return all candidates from all searches
        all_candidates = []
        for search_data in self.active_searches.values():
            all_candidates.extend(search_data.get("candidates", []))

        # Sort by score
        all_candidates.sort(key=lambda x: x.score or 0, reverse=True)

        return all_candidates


# Global search service instance
search_service = SearchService()
