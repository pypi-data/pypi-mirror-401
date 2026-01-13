"""Passage hierarchy models: Passage -> Phrase -> Concept."""

from typing import Literal

from pydantic import BaseModel, Field

from .enums import DocumentType


class DocumentClassification(BaseModel):
    """LLM response model for document type classification."""

    model_config = {"extra": "forbid"}

    document_type: DocumentType = Field(
        description="Document classification: research, technical, business, marketing, or general"
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="Classification confidence level"
    )
    reasoning: str = Field(
        description="Brief explanation (1-2 sentences) for the classification"
    )


class Concept(BaseModel):
    """Core concept within a phrase (2-5 words) - positions relative to parent phrase.text."""

    id: int = Field(description="Unique concept identifier")
    text: str = Field(description="2-5 word concept extracted from phrase")
    start: int = Field(description="Character offset in phrase.text where concept begins")
    stop: int = Field(description="Character offset in phrase.text where concept ends")
    reason: str = Field(
        default="",
        description="Why important (Linchpin, Actionable keyword, Technical anchor, Novel framework)",
    )


class Phrase(BaseModel):
    """Key phrase within a passage - positions relative to parent passage.text."""

    id: int = Field(description="Unique phrase identifier")
    text: str = Field(description="Sentence or fragment extracted from passage")
    start: int = Field(description="Character offset in passage.text where phrase begins")
    stop: int = Field(description="Character offset in passage.text where phrase ends")
    reason: str = Field(
        default="",
        description="Role (Core insight, Actionable, Perspective shift, Surprise)",
    )
    concepts: list[Concept] = Field(default_factory=list, description="Nested concepts extracted from this phrase")


class Passage(BaseModel):
    """Important passage from source document."""

    id: int = Field(description="Unique passage identifier")
    page: int = Field(description="Page number where passage appears")
    text: str = Field(description="Substantial passage (typically 150-300 words) extracted from document")
    reason: str = Field(description="Why selected (Forte criteria: Inspiring, Useful, Personal, Surprising)")
    phrases: list[Phrase] = Field(default_factory=list, description="Nested phrases extracted from this passage")
