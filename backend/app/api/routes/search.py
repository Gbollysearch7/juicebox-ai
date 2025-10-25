"""
Search API routes
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.schemas import (
    SearchRequest,
    SearchResponse,
    SearchStatusResponse,
    ErrorResponse
)
from app.services.search_service import search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.post(
    "",
    response_model=SearchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new candidate search",
    description="Start a new AI-powered candidate search based on natural language query and criteria"
)
async def create_search(request: SearchRequest):
    """
    Create a new candidate search.

    - **query**: Natural language description of candidates you're looking for
    - **count**: Number of candidates to find (1-100)
    - **entity**: Type of entity (person, company, etc.)
    - **criteria**: List of verification criteria
    - **enrichments**: List of data enrichment requests

    Returns a search_id that can be used to check status and retrieve results.
    """
    try:
        response = await search_service.create_search(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create search: {str(e)}"
        )


@router.get(
    "/{search_id}",
    response_model=SearchStatusResponse,
    summary="Get search status and results",
    description="Retrieve the current status and results of a candidate search"
)
async def get_search_status(search_id: str):
    """
    Get search status and results.

    - **search_id**: The unique ID returned when creating a search

    Returns current status, progress, and any candidates found so far.
    """
    result = await search_service.get_search_status(search_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search with ID {search_id} not found"
        )

    return result


@router.get(
    "",
    response_model=List[SearchStatusResponse],
    summary="List all searches",
    description="Get a list of all searches with their current status"
)
async def list_searches():
    """
    List all searches.

    Returns a list of all searches created in this session.
    """
    searches = await search_service.list_all_searches()
    return searches
