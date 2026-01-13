"""Executive summary models."""

from pydantic import BaseModel, Field


class ExecutiveSummaryBullet(BaseModel):
    """Single bullet point for executive summary."""

    text: str = Field(description="10-20 word distilled insight capturing essence")
    source_phrase: str = Field(description="Original phrase this insight came from")
    theme: str = Field(description="1-2 word theme categorizing this insight")


class ExecutiveSummaryLLMOutput(BaseModel):
    """LLM output model for executive summary (no metadata field).

    OpenAI structured outputs requires additionalProperties: false on all objects,
    which dict fields can't satisfy. Use this for LLM calls, then convert to
    ExecutiveSummary with metadata via ExecutiveSummary.from_llm_output().
    """

    summary: str = Field(description="2-3 sentence prose summary capturing document essence (not quotes)")
    bullets: list[ExecutiveSummaryBullet] = Field(description="Exactly 7 structured bullet points with text, themes, and sources")


class ExecutiveSummary(BaseModel):
    """Executive summary with prose paragraph, structured bullet points, and metadata.

    For LLM calls, use ExecutiveSummaryLLMOutput instead (no metadata field).
    Convert via ExecutiveSummary.from_llm_output() after LLM call.
    """

    summary: str = Field(description="2-3 sentence prose summary capturing document essence (not quotes)")
    bullets: list[ExecutiveSummaryBullet] = Field(description="Exactly 7 structured bullet points with text, themes, and sources")
    metadata: dict = Field(
        default_factory=dict,
        description="Reduction metrics (e.g., '1368::150::7' for phrases->filtered->insights), timestamps.",
    )

    @classmethod
    def from_llm_output(cls, llm_output: ExecutiveSummaryLLMOutput, metadata: dict | None = None) -> "ExecutiveSummary":
        """Create ExecutiveSummary from LLM output with optional metadata."""
        return cls(
            summary=llm_output.summary,
            bullets=llm_output.bullets,
            metadata=metadata or {},
        )
