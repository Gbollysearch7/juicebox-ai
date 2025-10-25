"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class EntityTypeEnum(str, Enum):
    """Entity types for search"""
    PERSON = "person"
    COMPANY = "company"
    RESEARCH_PAPER = "research_paper"
    ARTICLE = "article"


class SearchStatus(str, Enum):
    """Search status enum"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


# Request Models
class SearchRequest(BaseModel):
    """Request model for creating a candidate search"""
    query: str = Field(..., description="Natural language search query", min_length=3)
    count: int = Field(10, description="Number of candidates to find", ge=1, le=100)
    entity: EntityTypeEnum = Field(EntityTypeEnum.PERSON, description="Type of entity to search for")
    criteria: List[str] = Field(default_factory=list, description="Verification criteria")
    exclude_criteria: List[str] = Field(default_factory=list, description="Exclusion criteria")
    enrichments: List[str] = Field(default_factory=list, description="Data enrichment requests")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Senior ML Engineers at AI startups in San Francisco",
                "count": 10,
                "entity": "person",
                "criteria": [
                    "Has 5+ years of machine learning experience",
                    "Currently employed at a tech startup",
                    "Based in San Francisco Bay Area"
                ],
                "enrichments": [
                    "Find their LinkedIn profile",
                    "Extract current role and company"
                ]
            }
        }


class EnrichmentRequest(BaseModel):
    """Request model for data enrichment"""
    description: str = Field(..., description="What information to extract")
    format: str = Field("text", description="Output format: text or json")
    schema: Optional[Dict[str, Any]] = Field(None, description="JSON schema for structured output")


# Response Models
class CriteriaResult(BaseModel):
    """Verification criteria result"""
    description: str
    passed: bool
    reasoning: str
    references: List[str] = []


class VerificationResult(BaseModel):
    """Verification result for a candidate"""
    passed: bool
    criteria_results: List[CriteriaResult] = []


class EnrichmentResult(BaseModel):
    """Enrichment result"""
    description: str
    status: str
    result: Optional[Any] = None


class CandidateProperties(BaseModel):
    """Candidate properties"""
    name: Optional[str] = None
    current_role: Optional[str] = None
    current_company: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    experience_years: Optional[int] = None
    skills: List[str] = []


class Candidate(BaseModel):
    """Individual candidate result"""
    id: str
    url: str
    title: str
    status: str
    verification: Optional[VerificationResult] = None
    properties: CandidateProperties = Field(default_factory=CandidateProperties)
    enrichments: List[EnrichmentResult] = []
    score: Optional[float] = Field(None, description="AI-generated relevance score (0-100)")
    created_at: Optional[datetime] = None


class SearchResponse(BaseModel):
    """Response model for search creation"""
    search_id: str
    status: SearchStatus
    query: str
    count: int
    created_at: datetime
    message: str = "Search created successfully"


class SearchStatusResponse(BaseModel):
    """Response model for search status"""
    search_id: str
    status: SearchStatus
    query: str
    total_requested: int
    total_found: int
    candidates: List[Candidate] = []
    progress_percent: float = 0.0
    estimated_time_remaining: Optional[int] = None


class CandidateListResponse(BaseModel):
    """Response model for listing candidates"""
    total: int
    candidates: List[Candidate]


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
