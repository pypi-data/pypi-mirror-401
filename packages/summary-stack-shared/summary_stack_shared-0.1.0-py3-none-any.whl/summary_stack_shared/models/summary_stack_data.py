"""Unified SummaryStackData model stored in summary_stack JSONB column."""

from functools import cached_property

from pydantic import BaseModel, Field

from .executive_summary import ExecutiveSummary
from .passage import Concept, Passage
from .source_metadata import SourceMetadata


class SummaryStackData(BaseModel):
    """Unified summary stack data stored in summary_stack JSONB column.

    This is the single source of truth for all summary stack data.
    The database stores this as JSONB with additional table columns for indexing.
    """

    # Identity (first for easy reference)
    summary_stack_id: str = Field(description="UUID identifier")

    # Document metadata
    title: str | None = Field(default=None, description="Document title")

    # Source info and classification
    source_metadata: SourceMetadata = Field(description="Source info and classification")

    # Progressive summarization output
    executive_summary: ExecutiveSummary = Field(description="Prose + 7 bullets")

    # Full hierarchy with nested phrases/concepts
    passages: list[Passage] = Field(default_factory=list, description="Full hierarchy with nested phrases/concepts")

    @cached_property
    def unique_concepts(self) -> list[Concept]:
        """Extract deduplicated concepts from all passages.

        Traverses passages -> phrases -> concepts, deduplicating by text.
        Cached on first access - subsequent calls return cached result.
        """
        seen: set[str] = set()
        concepts: list[Concept] = []

        for passage in self.passages:
            for phrase in passage.phrases:
                for concept in phrase.concepts:
                    if concept.text not in seen:
                        seen.add(concept.text)
                        concepts.append(concept)

        return concepts
