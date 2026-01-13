"""Shared enumerations for Summary Stack."""

from enum import Enum


class SourceType(str, Enum):
    """Supported source types for content processing."""

    URL = "url"  # Web URLs (websites, PDFs at URLs, documents at URLs)
    PDF = "pdf"  # Local PDF files


class DocumentType(str, Enum):
    """Types of documents for specialized processing."""

    RESEARCH = "research"  # Papers, studies, academic content
    TECHNICAL = "technical"  # Documentation, specs, procedures
    BUSINESS = "business"  # Reports, strategies, metrics
    MARKETING = "marketing"  # Campaigns, positioning, audience insights
    GENERAL = "general"  # Default catch-all
