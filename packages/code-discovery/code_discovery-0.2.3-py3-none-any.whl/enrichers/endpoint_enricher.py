"""Endpoint enricher to extract detailed information from discovered endpoints."""

from pathlib import Path
from typing import List
from core.models import APIEndpoint, FrameworkType
from enrichers.base import BaseEnricher
from enrichers.java_spring_enricher import SpringBootEnricher
from enrichers.java_micronaut_enricher import MicronautEnricher
from enrichers.python_fastapi_enricher import FastAPIEnricher
from enrichers.python_flask_enricher import FlaskEnricher
from enrichers.dotnet_enricher import DotNetEnricher


class EndpointEnricher:
    """Enriches endpoints with detailed information from source code."""

    # Mapping of framework types to enricher classes
    FRAMEWORK_ENRICHERS = {
        FrameworkType.SPRING_BOOT: SpringBootEnricher,
        FrameworkType.MICRONAUT: MicronautEnricher,
        FrameworkType.FASTAPI: FastAPIEnricher,
        FrameworkType.FLASK: FlaskEnricher,
        FrameworkType.ASPNET_CORE: DotNetEnricher,
    }

    def __init__(self, repo_path: Path, framework: FrameworkType):
        """
        Initialize the endpoint enricher.

        Args:
            repo_path: Path to the repository root.
            framework: The framework type being analyzed.
        """
        self.repo_path = repo_path
        self.framework = framework
        
        # Get the appropriate enricher for this framework
        enricher_class = self.FRAMEWORK_ENRICHERS.get(framework)
        if enricher_class:
            self.enricher = enricher_class(repo_path)
        else:
            self.enricher = None

    def enrich_endpoints(self, endpoints: List[APIEndpoint]) -> List[APIEndpoint]:
        """
        Enrich a list of endpoints with detailed information.

        Args:
            endpoints: List of endpoints to enrich.

        Returns:
            List of enriched endpoints.
        """
        if not self.enricher:
            return endpoints
        
        enriched = []
        for endpoint in endpoints:
            enriched_endpoint = self.enrich_endpoint(endpoint)
            enriched.append(enriched_endpoint)
        return enriched

    def enrich_endpoint(self, endpoint: APIEndpoint) -> APIEndpoint:
        """
        Enrich a single endpoint with detailed information.

        Args:
            endpoint: The endpoint to enrich.

        Returns:
            Enriched endpoint.
        """
        if not self.enricher or not endpoint.source_file:
            return endpoint

        # Read the source file
        source_path = self.repo_path / endpoint.source_file
        if not source_path.exists():
            return endpoint

        try:
            content = source_path.read_text(encoding="utf-8")
        except Exception:
            return endpoint

        # Delegate to framework-specific enricher
        return self.enricher.enrich_endpoint(endpoint, content)

