"""ASP.NET Core framework detector."""

import re
from pathlib import Path
from typing import List
from detectors.base import BaseDetector
from core.models import FrameworkType


class DotNetDetector(BaseDetector):
    """Detector for ASP.NET Core applications."""

    def detect(self) -> bool:
        """Detect if ASP.NET Core is present in the repository."""
        indicators = [
            # Check for .NET project files
            self._check_csproj_files(),
            # Check for ASP.NET Core specific files
            self._check_aspnet_files(),
            # Check for ASP.NET Core code patterns
            self._check_aspnet_code(),
        ]

        return any(indicators)

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.ASPNET_CORE

    def get_source_paths(self) -> List[Path]:
        """Get paths to C# source files."""
        # Try multi-module discovery first
        source_paths = self._get_module_source_roots()

        # If multi-module discovery found paths, return them
        if source_paths:
            return source_paths

        # Fallback: Find .csproj files and get their directories
        csproj_files = self.find_files("*.csproj", max_depth=15)
        for csproj in csproj_files:
            # Validate it's a framework project
            if self._build_file_indicates_framework(csproj):
                source_paths.append(csproj.parent)

        # Last resort: Search for C# files recursively
        if not source_paths:
            cs_files = self.find_files("*.cs", max_depth=15)
            # Get unique parent directories
            parent_dirs = set(f.parent for f in cs_files)
            # Filter to directories that look like source roots
            for parent_dir in parent_dirs:
                if self._is_likely_source_directory(parent_dir):
                    source_paths.append(parent_dir)

        return source_paths

    def _get_build_file_patterns(self) -> List[str]:
        """Get build file patterns for .NET."""
        return ["*.csproj", "*.sln"]

    def _get_framework_indicators(self) -> List[str]:
        """Get framework indicators for ASP.NET Core."""
        return [
            "Microsoft.AspNetCore",
            "Microsoft.AspNetCore.Mvc",
            "Microsoft.AspNetCore.App",
            "Microsoft.NET.Sdk.Web",
        ]

    def _get_source_root_patterns(self) -> List[str]:
        """Get source root patterns for .NET."""
        # .NET projects typically have source files in project root (where .csproj is)
        # Return empty string to indicate project root itself
        return [""]

    def _get_module_source_roots(self) -> List[Path]:
        """
        Override to handle .NET's special case where source root is the project directory.
        """
        source_paths = []
        modules = self._extract_modules_from_build_files()

        for module_info in modules:
            # For .NET, the module directory IS the source root
            module_dir = module_info.directory
            if module_dir.exists():
                # Validate it's a source module
                if self._is_source_module(module_dir, module_info):
                    source_paths.append(module_dir)

        return source_paths

    def _is_source_module(self, source_root: Path, module_info) -> bool:
        """Validate ASP.NET Core source module."""
        if not source_root.exists():
            return False

        # For .NET, source_root is the project directory (where .csproj is)
        # Check if it contains C# files with ASP.NET Core code
        cs_files = list(source_root.rglob("*.cs"))
        if not cs_files:
            return False

        # Sample a few files to check for ASP.NET Core
        aspnet_patterns = [
            "[ApiController]",
            "ControllerBase",
            "Microsoft.AspNetCore.Mvc",
            "[HttpGet",
            "[HttpPost",
        ]

        for cs_file in cs_files[:10]:
            content = self.read_file(cs_file)
            if content:
                for pattern in aspnet_patterns:
                    if pattern in content:
                        return True

        return False

    def _is_likely_source_directory(self, directory: Path) -> bool:
        """Check if directory is likely a source directory with ASP.NET Core code."""
        cs_files = list(directory.rglob("*.cs"))
        if not cs_files:
            return False

        # Check a sample of files
        for cs_file in cs_files[:5]:
            content = self.read_file(cs_file)
            if content and ("[ApiController]" in content or "ControllerBase" in content):
                return True

        return False

    def _check_csproj_files(self) -> bool:
        """Check for ASP.NET Core or ASP.NET MVC Framework in .csproj files."""
        csproj_files = self.find_files("*.csproj", max_depth=15)

        # ASP.NET Core packages
        aspnet_core_packages = [
            "Microsoft.AspNetCore",
            "Microsoft.AspNetCore.Mvc",
            "Microsoft.AspNetCore.App",
            "Microsoft.NET.Sdk.Web",
        ]
        
        # ASP.NET MVC Framework packages (.NET Framework)
        aspnet_mvc_packages = [
            "Microsoft.AspNet.Mvc",
            "System.Web.Mvc",
            "Microsoft.AspNet.WebApi",
        ]
        
        # .NET Framework target frameworks
        framework_targets = [
            "net472",
            "net48",
            "net461",
            "net462",
            "net47",
            "net452",
            "net451",
            "net45",
            "net40",
        ]

        for csproj in csproj_files:
            content = self.read_file(csproj)
            if content:
                # Check for ASP.NET Core packages
                for package in aspnet_core_packages:
                    if package in content:
                        return True
                
                # Check for ASP.NET MVC Framework packages
                for package in aspnet_mvc_packages:
                    if package in content:
                        return True
                
                # Check for .NET Framework target framework
                for target in framework_targets:
                    if f'<TargetFramework>{target}</TargetFramework>' in content or f'<TargetFrameworks>{target}' in content:
                        # If it's a web project, likely ASP.NET MVC
                        if 'WebApplication' in content or 'WebSite' in content or 'Mvc' in content:
                            return True

        return False

    def _check_aspnet_files(self) -> bool:
        """Check for ASP.NET Core specific files."""
        aspnet_files = [
            "Program.cs",
            "Startup.cs",
            "appsettings.json",
            "appsettings.Development.json",
        ]

        for file_name in aspnet_files:
            files = self.find_files(file_name, max_depth=15)
            for file in files:
                content = self.read_file(file)
                if content and any(
                    keyword in content
                    for keyword in [
                        "WebApplication",
                        "UseRouting",
                        "UseEndpoints",
                        "AddControllers",
                        "MapControllers",
                    ]
                ):
                    return True

        return False

    def _check_aspnet_code(self) -> bool:
        """Check for ASP.NET Core or ASP.NET MVC Framework code patterns in C# files."""
        cs_files = self.find_files("*.cs", max_depth=15)

        # ASP.NET Core patterns
        aspnet_core_patterns = [
            "[ApiController]",
            "ControllerBase",
            "Microsoft.AspNetCore.Mvc",
        ]
        
        # ASP.NET MVC Framework patterns
        aspnet_mvc_patterns = [
            "System.Web.Mvc",
            ": Controller",
            "System.Web.Mvc.Controller",
            "[Route(",
            "[HttpGet",
            "[HttpPost",
            "[HttpPut",
            "[HttpDelete",
            "[ActionName(",
        ]

        for cs_file in cs_files[:50]:  # Limit for performance
            content = self.read_file(cs_file)
            if content:
                # Check for ASP.NET Core patterns
                for pattern in aspnet_core_patterns:
                    if pattern in content:
                        return True
                
                # Check for ASP.NET MVC Framework patterns
                for pattern in aspnet_mvc_patterns:
                    if pattern in content:
                        return True
                
                # Check for controller inheritance (both Core and Framework)
                if re.search(r':\s*Controller\b', content) or re.search(r':\s*ControllerBase\b', content):
                    return True

        return False

