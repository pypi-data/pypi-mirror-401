"""Search and list response models for Summary Stack."""

from datetime import datetime

from pydantic import BaseModel, Field

from .enums import SourceType


class StackListItem(BaseModel):
    """Lightweight stack item for list responses."""

    summary_stack_id: str
    title: str
    summary: str = Field(description="First 200 chars of summary")
    created_at: datetime
    source_type: SourceType | None = None
    source_domain: str | None = None


class StackListResponse(BaseModel):
    """Paginated list of stacks."""

    items: list[StackListItem]
    total: int
    limit: int
    offset: int


class StackSearchResult(BaseModel):
    """Single search result with similarity score."""

    summary_stack_id: str
    title: str
    summary: str
    similarity: float
    matching_chunks: list[str]
    source_type: SourceType | None = None
    source_domain: str | None = None


class StackSearchResponse(BaseModel):
    """Search results response."""

    query: str
    results: list[StackSearchResult]
    total_results: int


class StackSearchRequest(BaseModel):
    """Request model for search endpoint."""

    query: str = Field(min_length=1, max_length=500, description="Search query")
    limit: int = Field(default=10, ge=1, le=100, description="Max results to return")


class RelatedStackItem(BaseModel):
    """Related stack with similarity score."""

    summary_stack_id: str
    title: str
    summary: str
    similarity_score: float
    source_type: SourceType | None = None


class RelatedStacksResponse(BaseModel):
    """Related stacks response."""

    source_stack_id: str
    related: list[RelatedStackItem]
