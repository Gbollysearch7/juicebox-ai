"""
Candidates API routes
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from app.models.schemas import Candidate, CandidateListResponse
from app.services.search_service import search_service

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get(
    "",
    response_model=CandidateListResponse,
    summary="Get all candidates",
    description="Retrieve all candidates from all searches or from a specific search"
)
async def get_candidates(
    search_id: Optional[str] = Query(None, description="Filter by search ID"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum score filter"),
    verified_only: Optional[bool] = Query(False, description="Only return verified candidates")
):
    """
    Get all candidates with optional filters.

    - **search_id**: (Optional) Only return candidates from this search
    - **min_score**: (Optional) Only return candidates with score >= this value
    - **verified_only**: (Optional) Only return candidates that passed verification

    Returns a list of candidates sorted by score (highest first).
    """
    try:
        candidates = await search_service.get_candidates(search_id)

        # Apply filters
        if min_score is not None:
            candidates = [c for c in candidates if c.score and c.score >= min_score]

        if verified_only:
            candidates = [
                c for c in candidates
                if c.verification and c.verification.passed
            ]

        return CandidateListResponse(
            total=len(candidates),
            candidates=candidates
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve candidates: {str(e)}"
        )


@router.get(
    "/{candidate_id}",
    response_model=Candidate,
    summary="Get candidate by ID",
    description="Retrieve detailed information about a specific candidate"
)
async def get_candidate(candidate_id: str):
    """
    Get a specific candidate by ID.

    - **candidate_id**: The unique candidate ID

    Returns detailed candidate information including verification, properties, and enrichments.
    """
    # Get all candidates and find the matching one
    all_candidates = await search_service.get_candidates()

    candidate = next((c for c in all_candidates if c.id == candidate_id), None)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {candidate_id} not found"
        )

    return candidate
