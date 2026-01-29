"""Build file parsers for multi-module project discovery."""

import re
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from core.models import ModuleInfo


class BuildFileParser(ABC):
    """Abstract base class for parsing build files."""

    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """
        Check if this parser can handle the given file.

        Args:
            file_path: Path to the build file.

        Returns:
            bool: True if this parser can handle the file.
        """
        pass

    @abstractmethod
    def get_build_system(self) -> str:
        """
        Get the name of the build system this parser handles.

        Returns:
            str: Build system name (e.g., "gradle", "maven").
        """
        pass

    @abstractmethod
    def parse_modules(self, file_path: Path) -> List[str]:
        """
        Extract module names from a root build file.

        Args:
            file_path: Path to the root build file (e.g., settings.gradle, pom.xml).

        Returns:
            List[str]: List of module names/directories.
        """
        pass

    @abstractmethod
    def has_framework_dependency(
        self, file_path: Path, framework_indicators: List[str]
    ) -> bool:
        """
        Check if a build file indicates framework presence.

        Args:
            file_path: Path to the build file.
            framework_indicators: List of strings that indicate framework presence.

        Returns:
            bool: True if framework indicators are found.
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
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None


class GradleParser(BuildFileParser):
    """Parser for Gradle build files."""

    def can_parse(self, file_path: Path) -> bool:
        """Check if file is a Gradle build file."""
        name = file_path.name.lower()
        return name in ("build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts")

    def get_build_system(self) -> str:
        """Get build system name."""
        return "gradle"

    def parse_modules(self, file_path: Path) -> List[str]:
        """
        Parse settings.gradle to extract module names.

        Supports patterns:
        - include 'module1', 'module2'
        - include('module1', 'module2')
        - include 'module1'
        """
        content = self.read_file(file_path)
        if not content:
            return []

        modules = []

        # Pattern 1: include 'module1', 'module2', 'module3'
        pattern1 = r"include\s+['\"]([^'\"]+)['\"]"
        matches = re.findall(pattern1, content)
        modules.extend(matches)

        # Pattern 2: include('module1', 'module2')
        pattern2 = r"include\s*\(\s*['\"]([^'\"]+)['\"]"
        matches = re.findall(pattern2, content)
        modules.extend(matches)

        # Pattern 3: Multi-line include statements
        # Handle cases like:
        # include 'module1'
        # include 'module2'
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("include"):
                # Extract all quoted strings from the line
                quoted = re.findall(r"['\"]([^'\"]+)['\"]", line)
                modules.extend(quoted)

        return list(set(modules))  # Remove duplicates

    def has_framework_dependency(
        self, file_path: Path, framework_indicators: List[str]
    ) -> bool:
        """Check if build.gradle contains framework dependencies."""
        content = self.read_file(file_path)
        if not content:
            return False

        content_lower = content.lower()
        for indicator in framework_indicators:
            if indicator.lower() in content_lower:
                return True

        return False


class MavenParser(BuildFileParser):
    """Parser for Maven build files (pom.xml)."""

    def can_parse(self, file_path: Path) -> bool:
        """Check if file is a Maven pom.xml."""
        return file_path.name.lower() == "pom.xml"

    def get_build_system(self) -> str:
        """Get build system name."""
        return "maven"

    def parse_modules(self, file_path: Path) -> List[str]:
        """
        Parse pom.xml to extract module names from <modules> section.

        Handles both with and without XML namespaces.
        """
        content = self.read_file(file_path)
        if not content:
            return []

        modules = []

        try:
            # Try XML parsing first (more robust)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Handle namespace - Maven POMs use this namespace
            ns = {"maven": "http://maven.apache.org/POM/4.0.0"}

            # Try with namespace first
            modules_elem = root.find(".//maven:modules", ns)
            if modules_elem is None:
                # Try without namespace (some POMs don't use it)
                modules_elem = root.find(".//modules")

            if modules_elem is not None:
                for module_elem in modules_elem.findall("maven:module", ns):
                    if module_elem.text:
                        modules.append(module_elem.text.strip())

                # Also try without namespace
                if not modules:
                    for module_elem in modules_elem.findall("module"):
                        if module_elem.text:
                            modules.append(module_elem.text.strip())

        except Exception:
            # Fallback to regex parsing
            pattern = r"<module>([^<]+)</module>"
            matches = re.findall(pattern, content)
            modules.extend([m.strip() for m in matches])

        return list(set(modules))  # Remove duplicates

    def has_framework_dependency(
        self, file_path: Path, framework_indicators: List[str]
    ) -> bool:
        """Check if pom.xml contains framework dependencies."""
        content = self.read_file(file_path)
        if not content:
            return False

        content_lower = content.lower()
        for indicator in framework_indicators:
            if indicator.lower() in content_lower:
                return True

        return False


class PythonBuildParser(BuildFileParser):
    """Parser for Python build files (requirements.txt, pyproject.toml, setup.py)."""

    def can_parse(self, file_path: Path) -> bool:
        """Check if file is a Python build file."""
        name = file_path.name.lower()
        return name in ("requirements.txt", "pyproject.toml", "setup.py", "pipfile")

    def get_build_system(self) -> str:
        """Get build system name."""
        return "python"

    def parse_modules(self, file_path: Path) -> List[str]:
        """
        Python projects are typically single-module, but we can detect
        subdirectories with their own build files.

        For now, return empty list as Python multi-module is less common.
        """
        # Python projects are typically single-module
        # Multi-module Python projects would have separate requirements.txt
        # in subdirectories, which we'll discover via file search
        return []

    def has_framework_dependency(
        self, file_path: Path, framework_indicators: List[str]
    ) -> bool:
        """Check if Python build file contains framework dependencies."""
        content = self.read_file(file_path)
        if not content:
            return False

        content_lower = content.lower()
        for indicator in framework_indicators:
            # For requirements.txt, check for exact package name
            if file_path.name.lower() == "requirements.txt":
                # Pattern: framework-name==version or framework-name
                pattern = rf"^{re.escape(indicator.lower())}(==|>=|<=|>|<|~=)?"
                if re.search(pattern, content_lower, re.MULTILINE):
                    return True
            else:
                # For pyproject.toml, setup.py, Pipfile - simple substring match
                if indicator.lower() in content_lower:
                    return True

        return False


class DotNetParser(BuildFileParser):
    """Parser for .NET build files (.csproj, .sln)."""

    def can_parse(self, file_path: Path) -> bool:
        """Check if file is a .NET build file."""
        name = file_path.name.lower()
        return name.endswith(".csproj") or name.endswith(".sln")

    def get_build_system(self) -> str:
        """Get build system name."""
        return "dotnet"

    def parse_modules(self, file_path: Path) -> List[str]:
        """
        Parse .sln file to extract project paths.

        .csproj files represent single projects, so return empty for those.
        """
        if file_path.name.lower().endswith(".csproj"):
            # Single project file, no modules
            return []

        # Parse .sln file
        content = self.read_file(file_path)
        if not content:
            return []

        projects = []
        # Solution file format: Project("{guid}") = "Name", "Path\To\Project.csproj", "{guid}"
        pattern = r'Project\("[^"]+"\)\s*=\s*"[^"]+",\s*"([^"]+\.csproj)"'
        matches = re.findall(pattern, content)
        projects.extend(matches)

        return list(set(projects))

    def has_framework_dependency(
        self, file_path: Path, framework_indicators: List[str]
    ) -> bool:
        """Check if .csproj contains framework dependencies."""
        if not file_path.name.lower().endswith(".csproj"):
            return False

        content = self.read_file(file_path)
        if not content:
            return False

        content_lower = content.lower()
        for indicator in framework_indicators:
            if indicator.lower() in content_lower:
                return True

        return False


class BuildFileParserRegistry:
    """Registry for build file parsers."""

    def __init__(self):
        """Initialize with default parsers."""
        self._parsers: List[BuildFileParser] = [
            GradleParser(),
            MavenParser(),
            PythonBuildParser(),
            DotNetParser(),
        ]

    def get_parser(self, file_path: Path) -> Optional[BuildFileParser]:
        """
        Get the appropriate parser for a build file.

        Args:
            file_path: Path to the build file.

        Returns:
            Optional[BuildFileParser]: Parser instance, or None if no parser found.
        """
        for parser in self._parsers:
            if parser.can_parse(file_path):
                return parser
        return None

    def register_parser(self, parser: BuildFileParser):
        """
        Register a custom parser.

        Args:
            parser: Parser instance to register.
        """
        self._parsers.append(parser)


