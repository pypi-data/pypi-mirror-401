"""Spring Boot framework detector."""

from pathlib import Path
from typing import List
from detectors.base import BaseDetector
from core.models import FrameworkType


class SpringBootDetector(BaseDetector):
    """Detector for Spring Boot applications."""

    def detect(self) -> bool:
        """Detect if Spring Boot is present in the repository."""
        # Check for common Spring Boot indicators
        indicators = [
            # Maven
            self._check_maven_spring_boot(),
            # Gradle
            self._check_gradle_spring_boot(),
            # Spring Boot annotations in source files
            self._check_spring_annotations(),
        ]

        return any(indicators)

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.SPRING_BOOT

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
                # Check if this looks like a source directory (has .java files with framework annotations)
                if self._is_likely_source_directory(parent_dir):
                    source_paths.append(parent_dir)

        return source_paths

    def _get_build_file_patterns(self) -> List[str]:
        """Get build file patterns for Spring Boot."""
        return ["build.gradle*", "pom.xml"]

    def _get_framework_indicators(self) -> List[str]:
        """Get framework indicators for Spring Boot."""
        return [
            "spring-boot-starter-web",
            "spring-boot-starter",
            "spring-boot-parent",
            "org.springframework.boot",
        ]

    def _get_source_root_patterns(self) -> List[str]:
        """Get source root patterns for Java/Spring Boot."""
        return ["src/main/java"]

    def _is_source_module(self, source_root: Path, module_info) -> bool:
        """Validate Spring Boot source module."""
        if not source_root.exists() or not source_root.is_dir():
            return False

        # Check if directory contains Java files with Spring Boot annotations
        java_files = list(source_root.rglob("*.java"))
        if not java_files:
            return False

        # Sample a few files to check for Spring Boot annotations
        spring_annotations = [
            "@RestController",
            "@Controller",
            "@RequestMapping",
            "@GetMapping",
            "@PostMapping",
            "@PutMapping",
            "@DeleteMapping",
            "@PatchMapping",
        ]

        # Check up to 10 files for performance
        for java_file in java_files[:10]:
            content = self.read_file(java_file)
            if content:
                for annotation in spring_annotations:
                    if annotation in content:
                        return True  # Found Spring Boot code

        return False

    def _is_likely_source_directory(self, directory: Path) -> bool:
        """Check if directory is likely a source directory with Spring Boot code."""
        java_files = list(directory.rglob("*.java"))
        if not java_files:
            return False

        # Check a sample of files
        for java_file in java_files[:5]:
            content = self.read_file(java_file)
            if content and ("@RestController" in content or "@Controller" in content):
                return True

        return False

    def _check_maven_spring_boot(self) -> bool:
        """Check for Spring Boot in Maven configuration (supports Spring Boot 2.7.5 through 3.5.x)."""
        pom_files = self.find_files("pom.xml", max_depth=15)

        for pom in pom_files:
            content = self.read_file(pom)
            if content:
                # Check for Spring Boot parent or dependencies
                spring_boot_indicators = [
                    "spring-boot-starter-web",
                    "spring-boot-starter",
                    "spring-boot-parent",
                    "org.springframework.boot",
                ]
                for indicator in spring_boot_indicators:
                    if indicator in content:
                        return True

        return False

    def _check_gradle_spring_boot(self) -> bool:
        """Check for Spring Boot in Gradle configuration (supports Spring Boot 2.7.5 through 3.5.x)."""
        gradle_files = self.find_files("build.gradle*", max_depth=15)
        gradle_files.extend(self.find_files("settings.gradle*", max_depth=15))

        for gradle_file in gradle_files:
            content = self.read_file(gradle_file)
            if content:
                # Check for Spring Boot plugin or dependencies
                spring_boot_indicators = [
                    "spring-boot-starter-web",
                    "org.springframework.boot",
                    "id 'org.springframework.boot'",
                    'id("org.springframework.boot")',
                ]
                for indicator in spring_boot_indicators:
                    if indicator in content:
                        return True

        return False

    def _check_spring_annotations(self) -> bool:
        """Check for Spring Boot annotations in source files (supports Spring Boot 2.7.5 through 3.5.x)."""
        # Look for files with Spring Boot annotations
        java_files = self.find_files("*.java", max_depth=15)

        spring_annotations = [
            "@SpringBootApplication",
            "@RestController",
            "@Controller",
            "@RequestMapping",
            "@GetMapping",
            "@PostMapping",
            "@PutMapping",
            "@DeleteMapping",
            "@PatchMapping",
        ]

        for java_file in java_files[:50]:  # Limit to first 50 files for performance
            content = self.read_file(java_file)
            if content:
                for annotation in spring_annotations:
                    if annotation in content:
                        return True

        return False

