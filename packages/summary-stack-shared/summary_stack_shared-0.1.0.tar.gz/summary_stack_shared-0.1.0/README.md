# Summary Stack Shared

Shared Pydantic models for Summary Stack backend packages.

## Models

- `SummaryStackData` - Unified summary stack data stored in JSONB
- `Passage`, `Phrase`, `Concept` - Progressive summarization hierarchy
- `ExecutiveSummary`, `ExecutiveSummaryBullet` - Executive summary models
- `SourceMetadata` - Source metadata model
- `SourceType`, `DocumentType` - Enumerations

## Usage

```python
from summary_stack_shared import (
    SummaryStackData,
    Passage,
    Phrase,
    Concept,
    ExecutiveSummary,
    SourceMetadata,
    SourceType,
    DocumentType,
)
```
