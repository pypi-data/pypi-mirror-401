"""Flask endpoint enricher."""

from pathlib import Path
from typing import Optional
from enrichers.base import BaseEnricher
from core.models import APIEndpoint, FrameworkType


class FlaskEnricher(BaseEnricher):
    """Enricher for Flask endpoints."""

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.FLASK

    def enrich_endpoint(self, endpoint: APIEndpoint, content: str) -> APIEndpoint:
        """Enrich Flask endpoint."""
        # Flask parser already extracts basic info, but we can enhance:
        # - Better request body detection from function body
        # - Response schema from return statements
        # - Query parameter detection from request.args usage
        return endpoint

