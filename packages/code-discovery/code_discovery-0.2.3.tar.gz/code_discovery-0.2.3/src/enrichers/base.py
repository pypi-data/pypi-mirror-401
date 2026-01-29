"""Base class for endpoint enrichers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from core.models import APIEndpoint, FrameworkType


class BaseEnricher(ABC):
    """Abstract base class for endpoint enrichers."""

    def __init__(self, repo_path: Path):
        """
        Initialize the enricher.

        Args:
            repo_path: Path to the repository root.
        """
        self.repo_path = repo_path

    @abstractmethod
    def get_framework_type(self) -> FrameworkType:
        """
        Get the framework type this enricher handles.

        Returns:
            FrameworkType: The framework type.
        """
        pass

    @abstractmethod
    def enrich_endpoint(self, endpoint: APIEndpoint, content: str) -> APIEndpoint:
        """
        Enrich a single endpoint with detailed information.

        Args:
            endpoint: The endpoint to enrich.
            content: The source file content.

        Returns:
            Enriched endpoint.
        """
        pass

    def read_file(self, file_path: Path) -> Optional[str]:
        """
        Read file content.

        Args:
            file_path: Path to the file.

        Returns:
            Optional[str]: File content, or None if error.
        """
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception:
            return None

