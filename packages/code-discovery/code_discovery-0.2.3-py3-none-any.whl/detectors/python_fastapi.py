"""FastAPI framework detector."""

from pathlib import Path
from typing import List
from detectors.base import BaseDetector
from core.models import FrameworkType


class FastAPIDetector(BaseDetector):
    """Detector for FastAPI applications."""

    def detect(self) -> bool:
        """Detect if FastAPI is present in the repository."""
        indicators = [
            # Check dependency files
            self._check_requirements(),
            self._check_pyproject(),
            self._check_pipfile(),
            # Check for FastAPI imports in source files
            self._check_fastapi_imports(),
        ]

        return any(indicators)

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.FASTAPI

    def get_source_paths(self) -> List[Path]:
        """Get paths to Python source files."""
        # Try multi-module discovery first
        source_paths = self._get_module_source_roots()

        # If multi-module discovery found paths, return them
        if source_paths:
            return source_paths

        # Fallback: Check for single-module structure
        common_paths = [
            "app",
            "src",
            "api",
        ]

        for path in common_paths:
            full_path = self.repo_path / path
            if full_path.exists():
                source_paths.append(full_path)

        # Also check for root-level main files
        root_files = ["main.py", "app.py"]
        for root_file in root_files:
            full_path = self.repo_path / root_file
            if full_path.exists():
                source_paths.append(full_path.parent)

        # Last resort: Search for Python files recursively
        if not source_paths:
            py_files = self.find_files("*.py", max_depth=15)
            # Filter out venv, __pycache__, etc.
            py_files = [
                f
                for f in py_files
                if "venv" not in str(f) and "__pycache__" not in str(f)
            ]
            # Get unique parent directories
            parent_dirs = set(f.parent for f in py_files)
            # Filter to directories that look like source roots
            for parent_dir in parent_dirs:
                if self._is_likely_source_directory(parent_dir):
                    source_paths.append(parent_dir)

        return source_paths

    def _get_build_file_patterns(self) -> List[str]:
        """Get build file patterns for FastAPI."""
        return ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]

    def _get_framework_indicators(self) -> List[str]:
        """Get framework indicators for FastAPI."""
        return ["fastapi", "from fastapi import", "import fastapi"]

    def _get_source_root_patterns(self) -> List[str]:
        """Get source root patterns for Python/FastAPI."""
        return ["src", "app", "api"]

    def _is_source_module(self, source_root: Path, module_info) -> bool:
        """Validate FastAPI source module."""
        if not source_root.exists():
            return False

        # Check if it's a file (main.py, app.py) or directory
        if source_root.is_file():
            content = self.read_file(source_root)
            return content and ("fastapi" in content.lower() or "FastAPI(" in content)

        if not source_root.is_dir():
            return False

        # Check if directory contains Python files with FastAPI imports
        py_files = list(source_root.rglob("*.py"))
        if not py_files:
            return False

        # Sample a few files to check for FastAPI
        for py_file in py_files[:10]:
            content = self.read_file(py_file)
            if content:
                if "from fastapi import" in content or "import fastapi" in content or "FastAPI(" in content:
                    return True

        return False

    def _is_likely_source_directory(self, directory: Path) -> bool:
        """Check if directory is likely a source directory with FastAPI code."""
        py_files = list(directory.rglob("*.py"))
        if not py_files:
            return False

        # Check a sample of files
        for py_file in py_files[:5]:
            content = self.read_file(py_file)
            if content and ("from fastapi import" in content or "FastAPI(" in content):
                return True

        return False

    def _check_requirements(self) -> bool:
        """Check for FastAPI in requirements files."""
        req_files = [
            "requirements.txt",
            "requirements/base.txt",
            "requirements/production.txt",
            "requirements/dev.txt",
        ]

        for req_file in req_files:
            if self.check_dependency(req_file, "fastapi"):
                return True

        return False

    def _check_pyproject(self) -> bool:
        """Check for FastAPI in pyproject.toml."""
        if self.check_dependency("pyproject.toml", "fastapi"):
            return True
        return False

    def _check_pipfile(self) -> bool:
        """Check for FastAPI in Pipfile."""
        if self.check_dependency("Pipfile", "fastapi"):
            return True
        return False

    def _check_fastapi_imports(self) -> bool:
        """Check for FastAPI imports in Python source files."""
        py_files = self.find_files("*.py", max_depth=15)
        # Filter out venv and __pycache__
        py_files = [f for f in py_files if "venv" not in str(f) and "__pycache__" not in str(f)]

        fastapi_imports = [
            "from fastapi import",
            "import fastapi",
            "FastAPI(",
        ]

        for py_file in py_files[:50]:  # Limit for performance
            content = self.read_file(py_file)
            if content:
                for import_stmt in fastapi_imports:
                    if import_stmt in content:
                        return True

        return False

