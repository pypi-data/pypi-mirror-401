"""FastAPI endpoint enricher."""

from pathlib import Path
from typing import Optional
from enrichers.base import BaseEnricher
from core.models import APIEndpoint, FrameworkType


class FastAPIEnricher(BaseEnricher):
    """Enricher for FastAPI endpoints."""

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.FASTAPI

    def enrich_endpoint(self, endpoint: APIEndpoint, content: str) -> APIEndpoint:
        """Enrich FastAPI endpoint."""
        # FastAPI parser already extracts most information, but we can enhance:
        # - Better Pydantic model schema extraction
        # - Response status codes from decorators
        # - Tags from routers
        return endpoint

