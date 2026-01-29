"""Base class for framework detectors."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from core.models import FrameworkType, ModuleInfo
from utils.build_parsers import BuildFileParserRegistry


class BaseDetector(ABC):
    """Abstract base class for framework detectors."""

    def __init__(self, repo_path: str):
        """
        Initialize the detector.

        Args:
            repo_path: Path to the repository root.
        """
        self.repo_path = Path(repo_path)

    @abstractmethod
    def detect(self) -> bool:
        """
        Detect if this framework is present in the repository.

        Returns:
            bool: True if framework is detected, False otherwise.
        """
        pass

    @abstractmethod
    def get_framework_type(self) -> FrameworkType:
        """
        Get the framework type.

        Returns:
            FrameworkType: The type of framework this detector handles.
        """
        pass

    @abstractmethod
    def get_source_paths(self) -> List[Path]:
        """
        Get paths to source files that should be analyzed.

        Returns:
            List[Path]: List of paths to source files or directories.
        """
        pass

    def file_exists(self, relative_path: str) -> bool:
        """
        Check if a file exists in the repository.

        Args:
            relative_path: Path relative to repository root.

        Returns:
            bool: True if file exists, False otherwise.
        """
        return (self.repo_path / relative_path).exists()

    def find_files(self, pattern: str, max_depth: int = 10) -> List[Path]:
        """
        Find files matching a pattern in the repository.

        Args:
            pattern: Glob pattern to match files.
            max_depth: Maximum directory depth to search.

        Returns:
            List[Path]: List of matching file paths.
        """
        results = []
        try:
            for path in self.repo_path.rglob(pattern):
                # Calculate depth
                depth = len(path.relative_to(self.repo_path).parts)
                if depth <= max_depth and path.is_file():
                    results.append(path)
        except Exception as e:
            print(f"Error searching for files with pattern {pattern}: {e}")
        return results

    def read_file(self, file_path: Path) -> Optional[str]:
        """
        Read file content.

        Args:
            file_path: Path to the file.

        Returns:
            Optional[str]: File content, or None if error.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def check_dependency(self, dependency_file: str, dependency_name: str) -> bool:
        """
        Check if a dependency is present in a dependency file.

        Args:
            dependency_file: Path to dependency file (relative to repo root).
            dependency_name: Name of the dependency to check.

        Returns:
            bool: True if dependency is found, False otherwise.
        """
        file_path = self.repo_path / dependency_file
        if not file_path.exists():
            return False

        content = self.read_file(file_path)
        if content:
            return dependency_name.lower() in content.lower()
        return False

    def _get_build_file_patterns(self) -> List[str]:
        """
        Get build file patterns to search for.

        Override in subclasses to provide framework-specific patterns.

        Returns:
            List[str]: List of glob patterns for build files.
        """
        return []

    def _get_framework_indicators(self) -> List[str]:
        """
        Get framework indicators to look for in build files.

        Override in subclasses to provide framework-specific indicators.

        Returns:
            List[str]: List of strings that indicate framework presence.
        """
        return []

    def _get_source_root_patterns(self) -> List[str]:
        """
        Get source root patterns relative to module directory.

        Override in subclasses to provide framework-specific patterns.

        Returns:
            List[str]: List of relative paths (e.g., ["src/main/java"]).
        """
        return []

    def _is_source_module(self, source_root: Path, module_info: ModuleInfo) -> bool:
        """
        Validate that a source root is a source module (not test-only).

        Override in subclasses for framework-specific validation.

        Args:
            source_root: Path to the source root directory.
            module_info: Information about the module.

        Returns:
            bool: True if this is a source module with framework code.
        """
        # Default: check if directory exists and is not empty
        if not source_root.exists() or not source_root.is_dir():
            return False

        # Check if directory has any files (not just empty)
        try:
            return any(source_root.iterdir())
        except Exception:
            return False

    def _find_framework_build_files(self) -> List[Path]:
        """
        Find all build files that indicate this framework.

        Returns:
            List[Path]: List of build file paths.
        """
        build_files = []
        patterns = self._get_build_file_patterns()

        if not patterns:
            return build_files

        for pattern in patterns:
            files = self.find_files(pattern, max_depth=15)
            for file in files:
                if self._build_file_indicates_framework(file):
                    build_files.append(file)

        return build_files

    def _build_file_indicates_framework(self, file_path: Path) -> bool:
        """
        Check if a build file indicates framework presence.

        Args:
            file_path: Path to the build file.

        Returns:
            bool: True if framework indicators are found.
        """
        registry = BuildFileParserRegistry()
        parser = registry.get_parser(file_path)

        if not parser:
            return False

        framework_indicators = self._get_framework_indicators()
        if not framework_indicators:
            return False

        return parser.has_framework_dependency(file_path, framework_indicators)

    def _extract_modules_from_build_files(self) -> List[ModuleInfo]:
        """
        Extract module information from build files.

        Returns:
            List[ModuleInfo]: List of discovered modules.
        """
        modules = []
        registry = BuildFileParserRegistry()

        # Find all build files
        build_files = self._find_framework_build_files()

        # Process each build file
        for build_file in build_files:
            parser = registry.get_parser(build_file)
            if not parser:
                continue

            module_dir = build_file.parent
            module_name = module_dir.name

            modules.append(
                ModuleInfo(
                    directory=module_dir,
                    build_file=build_file,
                    build_system=parser.get_build_system(),
                    module_name=module_name,
                )
            )

        # Also check root build files for multi-module projects
        root_modules = self._extract_modules_from_root_build_files(registry)
        modules.extend(root_modules)

        return modules

    def _extract_modules_from_root_build_files(
        self, registry: BuildFileParserRegistry
    ) -> List[ModuleInfo]:
        """
        Extract modules from root-level build files (e.g., settings.gradle, pom.xml).

        Args:
            registry: Build file parser registry.

        Returns:
            List[ModuleInfo]: List of modules discovered from root build files.
        """
        modules = []
        framework_indicators = self._get_framework_indicators()

        if not framework_indicators:
            return modules

        # Find root build files
        root_patterns = ["settings.gradle*", "pom.xml"]
        for pattern in root_patterns:
            files = self.find_files(pattern, max_depth=3)  # Root files are shallow
            for file in files:
                # Only process root-level files
                depth = len(file.relative_to(self.repo_path).parts)
                if depth > 2:  # Skip nested build files
                    continue

                parser = registry.get_parser(file)
                if not parser:
                    continue

                # Extract module names
                module_names = parser.parse_modules(file)

                for module_name in module_names:
                    module_dir = self.repo_path / module_name
                    if not module_dir.exists():
                        continue

                    # Check if module has framework build file
                    module_build_file = self._find_module_build_file(module_dir, parser)
                    if module_build_file:
                        # Verify module has framework dependencies
                        if parser.has_framework_dependency(
                            module_build_file, framework_indicators
                        ):
                            modules.append(
                                ModuleInfo(
                                    directory=module_dir,
                                    build_file=module_build_file,
                                    build_system=parser.get_build_system(),
                                    module_name=module_name,
                                )
                            )

        return modules

    def _find_module_build_file(
        self, module_dir: Path, parser
    ) -> Optional[Path]:
        """
        Find the build file for a module directory.

        Args:
            module_dir: Path to the module directory.
            parser: Parser instance to use for file detection.

        Returns:
            Optional[Path]: Path to build file, or None if not found.
        """
        # Try common build file names
        build_file_names = [
            "build.gradle",
            "build.gradle.kts",
            "pom.xml",
            "requirements.txt",
            "pyproject.toml",
        ]

        for name in build_file_names:
            build_file = module_dir / name
            if build_file.exists() and parser.can_parse(build_file):
                return build_file

        return None

    def _get_module_source_roots(self) -> List[Path]:
        """
        Get source roots for all discovered modules.

        Returns:
            List[Path]: List of source root paths.
        """
        source_paths = []
        modules = self._extract_modules_from_build_files()

        source_patterns = self._get_source_root_patterns()

        for module_info in modules:
            for pattern in source_patterns:
                source_root = module_info.directory / pattern
                if source_root.exists():
                    # Validate it's a source module
                    if self._is_source_module(source_root, module_info):
                        source_paths.append(source_root)
                        break  # Found source root for this module, move to next

        return source_paths

