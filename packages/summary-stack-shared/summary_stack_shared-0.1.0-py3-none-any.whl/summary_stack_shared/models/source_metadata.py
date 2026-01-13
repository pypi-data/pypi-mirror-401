"""Source metadata model."""

from typing import Literal

from pydantic import BaseModel, Field

from .enums import DocumentType, SourceType


class SourceMetadata(BaseModel):
    """Source metadata for content being processed.

    NOTE: Title is NOT in SourceMetadata - it's stored as a top-level field
    in SummaryStackData to avoid duplication.
    """

    # Core identification
    uri: str = Field(description="Original URI (URL or file path)")

    # Type classification (from LLM)
    document_type: DocumentType = Field(
        default=DocumentType.GENERAL,
        description="Document classification (research/technical/business/marketing/general)",
    )
    classification_confidence: Literal["high", "medium", "low"] | None = Field(
        default=None,
        description="LLM confidence in document type classification",
    )
    classification_reasoning: str | None = Field(
        default=None,
        description="LLM explanation for document type classification",
    )
    source_type: SourceType = Field(description="Type of source (URL, PDF, etc.)")

    # URL-specific fields (None for PDFs)
    source_domain: str | None = Field(default=None, description="Domain for URLs (e.g., 'docs.anthropic.com')")
    normalized_url: str | None = Field(default=None, description="Normalized/canonical URL")

    @property
    def document_type_str(self) -> str:
        """Get document type as string value.

        Handles both enum and string values of document_type field.
        Defaults to 'general' if document_type is None or empty.
        """
        if hasattr(self.document_type, "value"):
            return self.document_type.value
        return str(self.document_type or "general")
