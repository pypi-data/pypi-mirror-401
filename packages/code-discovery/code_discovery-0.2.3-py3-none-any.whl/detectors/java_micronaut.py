"""Micronaut framework detector."""

from pathlib import Path
from typing import List
from detectors.base import BaseDetector
from core.models import FrameworkType


class MicronautDetector(BaseDetector):
    """Detector for Micronaut applications."""

    def detect(self) -> bool:
        """Detect if Micronaut is present in the repository."""
        # Check for common Micronaut indicators
        indicators = [
            # Maven
            self._check_maven_micronaut(),
            # Gradle
            self._check_gradle_micronaut(),
            # Micronaut config files
            self._check_micronaut_config(),
            # Micronaut annotations in source files
            self._check_micronaut_annotations(),
        ]

        return any(indicators)

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.MICRONAUT

    def get_source_paths(self) -> List[Path]:
        """Get paths to Java source files."""
        # Try multi-module discovery first
        source_paths = self._get_module_source_roots()

        # If multi-module discovery found paths, return them
        if source_paths:
            return source_paths

        # Fallback: Check for single-module structure
        common_paths = [
            "src/main/java",
        ]

        for path in common_paths:
            full_path = self.repo_path / path
            if full_path.exists():
                source_paths.append(full_path)

        # Last resort: Search for Java files recursively
        if not source_paths:
            java_files = self.find_files("*.java", max_depth=15)
            # Get unique parent directories, but prefer src/main/java structure
            parent_dirs = set(f.parent for f in java_files)
            # Filter to directories that look like source roots
            for parent_dir in parent_dirs:
                if self._is_likely_source_directory(parent_dir):
                    source_paths.append(parent_dir)

        return source_paths

    def _get_build_file_patterns(self) -> List[str]:
        """Get build file patterns for Micronaut."""
        return ["build.gradle*", "pom.xml"]

    def _get_framework_indicators(self) -> List[str]:
        """Get framework indicators for Micronaut."""
        return [
            "micronaut-http-server-netty",
            "io.micronaut",
        ]

    def _get_source_root_patterns(self) -> List[str]:
        """Get source root patterns for Java/Micronaut."""
        return ["src/main/java"]

    def _is_source_module(self, source_root: Path, module_info) -> bool:
        """Validate Micronaut source module."""
        if not source_root.exists() or not source_root.is_dir():
            return False

        # Check if directory contains Java files with Micronaut annotations
        java_files = list(source_root.rglob("*.java"))
        if not java_files:
            return False

        # Sample a few files to check for Micronaut-specific annotations
        # Use Micronaut-specific annotations, not @Controller which Spring Boot also uses
        # Use parentheses to avoid matching @PostMapping, @PostConstruct, etc.
        micronaut_specific_annotations = [
            "@Get(",
            "@Post(",
            "@Put(",
            "@Delete(",
            "@Patch(",
            "io.micronaut.http.annotation",
        ]

        # Check up to 10 files for performance
        for java_file in java_files[:10]:
            content = self.read_file(java_file)
            if content:
                # Check for Micronaut-specific annotations
                for annotation in micronaut_specific_annotations:
                    if annotation in content:
                        return True  # Found Micronaut code
                
                # Check for Micronaut Controller import (more specific)
                if "io.micronaut.http.annotation.Controller" in content:
                    return True

        return False

    def _is_likely_source_directory(self, directory: Path) -> bool:
        """Check if directory is likely a source directory with Micronaut code."""
        java_files = list(directory.rglob("*.java"))
        if not java_files:
            return False

        # Check a sample of files for Micronaut-specific patterns
        # Use parentheses to avoid matching @PostMapping, @PostConstruct, etc.
        for java_file in java_files[:5]:
            content = self.read_file(java_file)
            if content:
                # Check for Micronaut-specific annotations or imports
                if any(
                    pattern in content
                    for pattern in [
                        "@Get(",
                        "@Post(",
                        "@Put(",
                        "@Delete(",
                        "io.micronaut.http.annotation",
                    ]
                ):
                    return True

        return False

    def _check_maven_micronaut(self) -> bool:
        """Check for Micronaut in Maven configuration."""
        if self.check_dependency("pom.xml", "micronaut-http-server-netty"):
            return True
        if self.check_dependency("pom.xml", "io.micronaut"):
            return True
        return False

    def _check_gradle_micronaut(self) -> bool:
        """Check for Micronaut in Gradle configuration."""
        gradle_files = [
            "build.gradle",
            "build.gradle.kts",
        ]

        for gradle_file in gradle_files:
            if self.check_dependency(gradle_file, "io.micronaut"):
                return True
            if self.check_dependency(gradle_file, "micronaut-http-server-netty"):
                return True

        return False

    def _check_micronaut_config(self) -> bool:
        """Check for Micronaut configuration files."""
        config_files = [
            "src/main/resources/application.yml",
            "src/main/resources/application.yaml",
            "src/main/resources/application.properties",
            "micronaut-cli.yml",
        ]

        for config_file in config_files:
            if self.file_exists(config_file):
                content = self.read_file(self.repo_path / config_file)
                if content and "micronaut" in content.lower():
                    return True

        return False

    def _check_micronaut_annotations(self) -> bool:
        """Check for Micronaut annotations in source files."""
        java_files = self.find_files("*.java", max_depth=15)

        # Micronaut-specific annotations (not shared with Spring Boot)
        # Use word boundaries to avoid matching @PostMapping, @PostConstruct, etc.
        micronaut_specific_annotations = [
            "@Get(",
            "@Post(",
            "@Put(",
            "@Delete(",
            "@Patch(",
            "@Options(",
            "@Head(",
            "@Trace(",
            "io.micronaut.http.annotation",
            "io.micronaut.http.server.annotation",
        ]

        for java_file in java_files[:50]:  # Limit to first 50 files for performance
            content = self.read_file(java_file)
            if content:
                # Check for Micronaut-specific annotations
                # Use word boundary matching to avoid false positives
                for annotation in micronaut_specific_annotations:
                    # Check if annotation appears as a standalone annotation (not part of another)
                    if annotation in content:
                        # For annotations with parentheses, they're more specific
                        if annotation.endswith('('):
                            if annotation in content:
                                return True
                        else:
                            # For package names, check they're not part of Spring imports
                            if annotation in content and "org.springframework" not in content[:content.find(annotation)+200]:
                                return True
                
                # Check for Micronaut imports (more specific than just @Controller)
                if "io.micronaut" in content and "@Controller" in content:
                    # Verify it's actually Micronaut's Controller, not Spring's
                    if "io.micronaut.http.annotation.Controller" in content:
                        return True

        return False

