"""Spring Boot API parser."""

import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from parsers.base import BaseParser
from core.models import (
    APIEndpoint,
    APIParameter,
    APIResponse,
    AuthenticationRequirement,
    AuthenticationType,
    DiscoveryResult,
    FrameworkType,
    HTTPMethod,
    ParameterLocation,
)


class SpringBootParser(BaseParser):
    """Parser for Spring Boot REST APIs."""

    def __init__(self, source_paths: List[Path], repo_path: Path):
        super().__init__(source_paths, repo_path)
        self._file_content_cache: Dict[Path, str] = {}

    def parse(self) -> DiscoveryResult:
        """Parse Spring Boot source files for API endpoints (Spring Boot 2.7.5 through 3.5.x)."""
        endpoints = []
        java_files = self.find_files("*.java")

        # First pass: cache all file contents for cross-file type resolution
        for java_file in java_files:
            content = self.read_file(java_file)
            if content:
                self._file_content_cache[java_file] = content

        # Second pass: parse controllers (now with full file cache available)
        # Create a copy of items to avoid modification during iteration
        cache_items = list(self._file_content_cache.items())
        for java_file, content in cache_items:
            if self._is_rest_controller(content):
                endpoints.extend(self._parse_controller(java_file, content))

        return DiscoveryResult(
            framework=FrameworkType.SPRING_BOOT,
            endpoints=endpoints,
            title="Spring Boot API",
        )

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.SPRING_BOOT

    def _is_rest_controller(self, content: str) -> bool:
        """Check if the class is a REST controller."""
        return "@RestController" in content or "@Controller" in content

    def _parse_controller(self, file_path: Path, content: str) -> List[APIEndpoint]:
        """Parse a controller file for endpoints."""
        endpoints = []
        
        # Extract class-level @RequestMapping
        class_path = self._extract_class_request_mapping(content, file_path)
        
        # Extract controller class name for tags and unique operationIds
        controller_name = self._extract_controller_name(content, file_path)
        
        # Find all method annotations
        methods = self._extract_methods(content, file_path)
        
        for method_info in methods:
            endpoint = self._create_endpoint(
                method_info,
                class_path,
                file_path,
                controller_name,
            )
            if endpoint:
                endpoints.append(endpoint)

        return endpoints

    def _extract_class_request_mapping(self, content: str, file_path: Path) -> str:
        """Extract class-level @RequestMapping path, resolving constants if needed."""
        # Match @RequestMapping("/path") or @RequestMapping(value = "/path")
        patterns = [
            r'@RequestMapping\s*\(\s*"([^"]+)"\s*\)',
            r'@RequestMapping\s*\(\s*value\s*=\s*"([^"]+)"\s*\)',
            r'@RequestMapping\s*\(\s*path\s*=\s*"([^"]+)"\s*\)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        
        # Check for constant references: @RequestMapping(ClassName.CONSTANT_NAME)
        constant_patterns = [
            r'@RequestMapping\s*\(\s*(\w+)\.(\w+)\s*\)',
            r'@RequestMapping\s*\(\s*value\s*=\s*(\w+)\.(\w+)\s*\)',
            r'@RequestMapping\s*\(\s*path\s*=\s*(\w+)\.(\w+)\s*\)',
        ]
        
        for pattern in constant_patterns:
            match = re.search(pattern, content)
            if match:
                class_name = match.group(1)
                constant_name = match.group(2)
                # Resolve the constant value
                constant_value = self._resolve_constant(class_name, constant_name, file_path)
                if constant_value:
                    return constant_value
        
        # Check for inheritance - if controller extends a base class with @RequestMapping
        base_class_path = self._extract_inherited_request_mapping(content, file_path)
        if base_class_path:
            return base_class_path
        
        return ""

    def _extract_methods(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Extract method information from controller (Spring Boot 2.7.5 through 3.5.x)."""
        methods = []
        
        # Patterns for different Spring annotations
        # Support both with and without path parameters
        mapping_patterns = [
            # @GetMapping("/path") or @GetMapping
            (r'@GetMapping\s*(?:\(\s*"([^"]+)"\s*\))?', HTTPMethod.GET),
            (r'@PostMapping\s*(?:\(\s*"([^"]+)"\s*\))?', HTTPMethod.POST),
            (r'@PutMapping\s*(?:\(\s*"([^"]+)"\s*\))?', HTTPMethod.PUT),
            (r'@DeleteMapping\s*(?:\(\s*"([^"]+)"\s*\))?', HTTPMethod.DELETE),
            (r'@PatchMapping\s*(?:\(\s*"([^"]+)"\s*\))?', HTTPMethod.PATCH),
        ]
        
        for pattern, default_method in mapping_patterns:
            for match in re.finditer(pattern, content):
                # Extract path if present (group 1), otherwise empty string
                path = match.group(1) if match.lastindex and match.lastindex >= 1 else ""
                
                # Extract method signature and body
                method_start = match.end()
                method_signature = self._extract_method_signature(content, method_start)
                
                # If no path specified, leave it empty (will use class path only)
                # Don't use method name as fallback for REST endpoints
                
                methods.append({
                    "path": path,
                    "method": default_method,
                    "signature": method_signature,
                    "position": match.start(),
                })
        
        # Handle @RequestMapping with method parameter (Spring Boot 2.x and 3.x)
        # Patterns: @RequestMapping(value = "/path", method = RequestMethod.GET)
        #           @RequestMapping(path = "/path", method = RequestMethod.POST)
        #           @RequestMapping("/path", method = RequestMethod.PUT)
        #           @RequestMapping(value = ClassName.CONSTANT, method = RequestMethod.GET)
        request_mapping_patterns = [
            # @RequestMapping(value = "/path", method = RequestMethod.GET)
            (r'@RequestMapping\s*\(\s*value\s*=\s*"([^"]+)"\s*,\s*method\s*=\s*RequestMethod\.(\w+)\s*\)', 1, 2, True),
            # @RequestMapping(path = "/path", method = RequestMethod.GET)
            (r'@RequestMapping\s*\(\s*path\s*=\s*"([^"]+)"\s*,\s*method\s*=\s*RequestMethod\.(\w+)\s*\)', 1, 2, True),
            # @RequestMapping("/path", method = RequestMethod.GET)
            (r'@RequestMapping\s*\(\s*"([^"]+)"\s*,\s*method\s*=\s*RequestMethod\.(\w+)\s*\)', 1, 2, True),
            # @RequestMapping(method = RequestMethod.GET, value = "/path")
            (r'@RequestMapping\s*\(\s*method\s*=\s*RequestMethod\.(\w+)\s*,\s*value\s*=\s*"([^"]+)"\s*\)', 2, 1, True),
            # @RequestMapping(method = RequestMethod.GET, path = "/path")
            (r'@RequestMapping\s*\(\s*method\s*=\s*RequestMethod\.(\w+)\s*,\s*path\s*=\s*"([^"]+)"\s*\)', 2, 1, True),
            # @RequestMapping(value = ClassName.CONSTANT, method = RequestMethod.GET)
            (r'@RequestMapping\s*\(\s*value\s*=\s*(\w+)\.(\w+)\s*,\s*method\s*=\s*RequestMethod\.(\w+)\s*\)', None, 3, False),
            # @RequestMapping(path = ClassName.CONSTANT, method = RequestMethod.GET)
            (r'@RequestMapping\s*\(\s*path\s*=\s*(\w+)\.(\w+)\s*,\s*method\s*=\s*RequestMethod\.(\w+)\s*\)', None, 3, False),
            # @RequestMapping(method = RequestMethod.GET) - no path
            (r'@RequestMapping\s*\(\s*method\s*=\s*RequestMethod\.(\w+)\s*\)', None, 1, True),
        ]
        
        for pattern, path_group, method_group, is_string_literal in request_mapping_patterns:
            for match in re.finditer(pattern, content):
                http_method_name = match.group(method_group).upper()
                try:
                    http_method = HTTPMethod[http_method_name]
                except KeyError:
                    continue  # Skip unsupported HTTP methods
                
                # Extract path if specified
                if path_group:
                    if is_string_literal:
                        path = match.group(path_group) if match.lastindex and path_group <= match.lastindex else ""
                    else:
                        # Constant reference: extract class and constant name
                        const_class = match.group(1)
                        const_name = match.group(2)
                        path = self._resolve_constant(const_class, const_name, file_path) or ""
                else:
                    path = ""
                
                # Extract method signature
                method_start = match.end()
                method_signature = self._extract_method_signature(content, method_start)
                
                # If no path specified, leave it empty (will use class path only)
                
                methods.append({
                    "path": path,
                    "method": http_method,
                    "signature": method_signature,
                    "position": match.start(),
                })
        
        return methods
    
    def _extract_method_name(self, signature: str) -> Optional[str]:
        """Extract method name from method signature."""
        # Pattern: find method name before opening parenthesis
        # Handle: public ReturnType methodName(params)
        match = re.search(r'(\w+)\s*\(', signature)
        if match:
            return match.group(1)
        return None

    def _extract_method_signature(self, content: str, start_pos: int) -> str:
        """Extract Java method signature after annotation, handling multi-line parameters."""
        # Look for method declaration start
        remaining = content[start_pos:]
        
        # Find method visibility modifier
        visibility_match = re.search(r'^(public|private|protected)\s+', remaining)
        if visibility_match:
            method_start_idx = visibility_match.start()
            after_visibility = visibility_match.end()
        else:
            method_start_idx = 0
            after_visibility = 0
        
        # Now find the method name - it's the last identifier before the opening paren
        # This handles nested generics in return types like ResponseEntity<List<Tutorial>>
        # Pattern: find identifier followed by opening paren
        method_name_pattern = r'(\w+)\s*\('
        method_name_match = re.search(method_name_pattern, remaining[after_visibility:])
        if not method_name_match:
            return ""
        
        # The opening paren is at after_visibility + method_name_match.end() - 1
        paren_start = after_visibility + method_name_match.end() - 1
        
        # Find matching closing parenthesis, handling nested parens and annotations
        paren_count = 0
        i = paren_start
        in_string = False
        string_char = None
        
        while i < len(remaining) and i < paren_start + 2000:  # Reasonable limit
            char = remaining[i]
            
            # Track string literals to avoid matching parens inside strings
            if char in ['"', "'"] and (i == 0 or remaining[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
            
            if not in_string:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        # Found matching closing paren - include it
                        method_end_idx = i + 1
                        return remaining[method_start_idx:method_end_idx]
            i += 1
        
        # Fallback: if we can't find matching paren, try single-line pattern
        method_pattern = r'(public|private|protected)?\s+[\w<>[\],\s]+\s+\w+\s*\([^)]*\)'
        match = re.search(method_pattern, remaining[:500])
        if match:
            return match.group(0)
        
        return ""

    def _create_endpoint(
        self,
        method_info: Dict[str, Any],
        class_path: str,
        file_path: Path,
        controller_name: str,
    ) -> Optional[APIEndpoint]:
        """Create an APIEndpoint from method information."""
        # Combine class path and method path
        full_path = self._combine_paths(class_path, method_info["path"])
        full_path = self.normalize_path(full_path)
        
        # Extract parameters from signature
        parameters = self._extract_parameters(method_info["signature"], full_path)
        
        # Extract request body if present
        request_body = self._extract_request_body(method_info["signature"], file_path)
        
        # Extract response schema from return type
        response_schema = self._extract_response_schema(method_info["signature"], file_path)
        
        # Extract method name for unique operationId
        method_name = self._extract_method_name(method_info["signature"])
        
        # Generate unique operationId using controller + method name
        operation_id = self._generate_operation_id(
            full_path, 
            method_info["method"], 
            controller_name=controller_name,
            method_name=method_name,
        )
        
        # Create endpoint with controller name as tag
        endpoint = APIEndpoint(
            path=full_path,
            method=method_info["method"],
            operation_id=operation_id,
            tags=[controller_name] if controller_name else [],
            parameters=parameters,
            request_body=request_body,
            responses=[
                APIResponse(
                    status_code=200,
                    description="Successful response",
                    schema=response_schema,
                )
            ],
            source_file=self.get_relative_path(file_path),
        )
        
        return endpoint

    def _combine_paths(self, base: str, path: str) -> str:
        """Combine base path and method path."""
        if not base:
            return path
        if not path:
            return base
        
        # Remove trailing slash from base and leading slash from path
        base = base.rstrip('/')
        path = path.lstrip('/')
        
        return f"{base}/{path}"

    def _extract_parameters(self, signature: str, path: str) -> List[APIParameter]:
        """Extract parameters from method signature."""
        parameters = []
        
        # Extract path parameters
        path_vars = self.extract_path_variables(path)
        for var in path_vars:
            # Try to find @PathVariable annotation with type
            # Handle both @PathVariable("id") long id and @PathVariable long id
            # Pattern 1: @PathVariable("id") Type id
            pattern1 = rf'@PathVariable\s*\([^)]*["\']?{var}["\']?[^)]*\)\s+(?:final\s+)?([\w<>[\],\s]+)\s+{var}'
            # Pattern 2: @PathVariable Type id (no quotes)
            pattern2 = rf'@PathVariable\s+(?:final\s+)?([\w<>[\],\s]+)\s+{var}'
            
            param_type = "string"
            match = re.search(pattern1, signature, re.MULTILINE | re.DOTALL)
            if match:
                param_type = self._java_type_to_openapi_type(match.group(1).strip())
            else:
                match = re.search(pattern2, signature, re.MULTILINE | re.DOTALL)
                if match:
                    param_type = self._java_type_to_openapi_type(match.group(1).strip())
            
            parameters.append(
                APIParameter(
                    name=var,
                    location=ParameterLocation.PATH,
                    required=True,
                    type=param_type,
                )
            )
        
        # Extract query parameters from @RequestParam with types
        # Handle both single-line and multi-line: @RequestParam(...)\n Type paramName
        # Pattern matches: @RequestParam(required = false) String title
        pattern = r'@RequestParam\s*(?:\(([^)]*)\))?\s+(?:final\s+)?([\w<>[\],\s]+)\s+(\w+)'
        for match in re.finditer(pattern, signature, re.MULTILINE | re.DOTALL):
            annotation_params = match.group(1) if match.group(1) else ""
            param_type = self._java_type_to_openapi_type(match.group(2).strip())
            param_name = match.group(3)
            if param_name not in path_vars:
                # Check if required (default is true for @RequestParam)
                # Look for required=false in the annotation parameters
                required = "required=false" not in annotation_params and "required = false" not in annotation_params
                parameters.append(
                    APIParameter(
                        name=param_name,
                        location=ParameterLocation.QUERY,
                        required=required,
                        type=param_type,
                    )
                )
        
        # Extract header parameters from @RequestHeader
        pattern = r'@RequestHeader\s*(?:\([^)]*\))?\s+(?:final\s+)?([\w<>[\],\s]+)\s+(\w+)'
        for match in re.finditer(pattern, signature):
            param_type = self._java_type_to_openapi_type(match.group(1).strip())
            param_name = match.group(2)
            parameters.append(
                APIParameter(
                    name=param_name,
                    location=ParameterLocation.HEADER,
                    required=False,
                    type=param_type,
                )
            )
        
        return parameters

    def _extract_request_body(self, signature: str, file_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
        """Extract request body from method signature."""
        # Look for @RequestBody annotation
        if "@RequestBody" not in signature:
            return None
        
        # Extract parameter type after @RequestBody
        # Handle multi-line: @RequestBody\n Type paramName
        pattern = r'@RequestBody\s+(?:@\w+\s+)*(?:final\s+)?([\w<>[\],\s]+)\s+\w+'
        match = re.search(pattern, signature, re.MULTILINE | re.DOTALL)
        if match:
            param_type = match.group(1).strip()
            schema = self._java_type_to_schema(param_type, file_path)
            return {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": schema,
                    }
                },
            }
        
        return None

    def _extract_response_schema(self, signature: str, file_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
        """Extract response schema from method return type."""
        # Extract return type from method signature
        # Pattern: public ReturnType methodName(...)
        # Need to capture the full return type including nested generics like ResponseEntity<List<Tutorial>>
        
        # Method signature format: [visibility] ReturnType methodName(params)
        # We need to extract ReturnType
        
        # Find visibility modifier (optional)
        visibility_match = re.search(r'^(public|private|protected)\s+', signature)
        if visibility_match:
            start_pos = visibility_match.end()
        else:
            # No visibility modifier, start from beginning
            start_pos = 0
        
        # Now we need to find where the method name starts
        # The method name comes after the return type and before the opening paren
        # We need to handle nested generics in the return type
        
        # Find the opening parenthesis of the method parameters
        # This marks the end of the return type + method name
        paren_pos = signature.find('(')
        if paren_pos == -1:
            return None
        
        # Extract everything from start_pos to paren_pos
        # This gives us: ReturnType methodName
        return_and_method = signature[start_pos:paren_pos].strip()
        
        # Now we need to separate return type from method name
        # Method name is the last word before the paren
        # But return type can have spaces and generics: ResponseEntity<List<Tutorial>>
        
        # Find the last word (method name) - it's the last identifier before the paren
        # Pattern: find last sequence of word characters
        method_name_match = re.search(r'(\w+)\s*$', return_and_method)
        if not method_name_match:
            return None
        
        method_name_start = method_name_match.start()
        return_type = return_and_method[:method_name_start].strip()
        
        # Skip void and HttpStatus
        if return_type in ["void", "Void", "HttpStatus"] or not return_type:
            return None
        
        # Parse the return type schema
        schema = self._java_type_to_schema(return_type, file_path)
        return schema

    def _java_type_to_openapi_type(self, java_type: str) -> str:
        """Convert Java type to OpenAPI type."""
        java_type = java_type.strip()
        type_map = {
            "int": "integer",
            "Integer": "integer",
            "long": "integer",
            "Long": "integer",
            "float": "number",
            "Float": "number",
            "double": "number",
            "Double": "number",
            "boolean": "boolean",
            "Boolean": "boolean",
            "String": "string",
            "char": "string",
            "Character": "string",
        }
        return type_map.get(java_type, "string")

    def _java_type_to_schema(self, java_type: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        """Convert Java type to OpenAPI schema, parsing model classes if available."""
        java_type = java_type.strip()

        # Handle generic types like List<String>, Map<String, Object>, ResponseEntity<List<T>>
        if "<" in java_type:
            # Extract base type and inner type(s)
            base_type = java_type.split("<")[0].strip()
            
            # Extract inner type - handle nested generics like ResponseEntity<List<Tutorial>>
            # Find the matching closing bracket
            inner_start = java_type.find("<") + 1
            bracket_count = 0
            inner_end = inner_start
            for i in range(inner_start, len(java_type)):
                if java_type[i] == '<':
                    bracket_count += 1
                elif java_type[i] == '>':
                    if bracket_count == 0:
                        inner_end = i
                        break
                    bracket_count -= 1
            
            inner_type = java_type[inner_start:inner_end].strip()
            
            if base_type in ["List", "ArrayList", "Set", "HashSet"]:
                # Parse inner type schema recursively
                inner_schema = self._java_type_to_schema(inner_type, file_path)
                return {"type": "array", "items": inner_schema}
            elif base_type in ["Map", "HashMap"]:
                return {"type": "object", "additionalProperties": True}
            elif base_type in ["ResponseEntity"]:
                # Handle ResponseEntity<T> or ResponseEntity<List<T>> - extract inner type recursively
                return self._java_type_to_schema(inner_type, file_path)

        # Handle simple types
        openapi_type = self._java_type_to_openapi_type(java_type)
        if openapi_type != "string":
            return {"type": openapi_type}

        # Try to find and parse the Java model class
        if file_path:
            model_schema = self._parse_java_model(java_type, file_path)
            if model_schema:
                return model_schema

        # Default to object for complex types
        return {"type": "object"}

    def _parse_java_model(self, class_name: str, controller_file: Path) -> Optional[Dict[str, Any]]:
        """
        Parse a Java model class to extract field definitions (supports Spring Boot 2.7.5 through 3.5.x).
        
        Searches the entire repository for model classes, not just source_paths, to handle
        multi-module projects where DTOs may be in separate modules (e.g., DTO module).
        """
        # First, check cached files (from source_paths) for quick lookup
        cached_files = list(self._file_content_cache.keys()) if self._file_content_cache else []
        
        # Search cached files first
        for java_file in cached_files:
            # Skip controller files
            if "controller" in str(java_file).lower() or "Controller" in java_file.name:
                continue
            
            content = self._file_content_cache[java_file]
            class_pattern = rf'public\s+class\s+{re.escape(class_name)}\b'
            if re.search(class_pattern, content):
                # Found in cache, extract schema
                return self._extract_schema_from_content(content)
        
        # Not found in cache, search entire repository
        # This handles multi-module projects where DTOs are in separate modules
        repo_java_files = list(self.repo_path.rglob("*.java"))
        
        for java_file in repo_java_files:
            # Skip controller files
            if "controller" in str(java_file).lower() or "Controller" in java_file.name:
                continue
            
            # Use cached content if available, otherwise read and cache
            if java_file in self._file_content_cache:
                content = self._file_content_cache[java_file]
            else:
                content = self.read_file(java_file)
                if content:
                    # Cache for future lookups
                    self._file_content_cache[java_file] = content
            
            if not content:
                continue
            
            # Check if this file contains the class we're looking for
            class_pattern = rf'public\s+class\s+{re.escape(class_name)}\b'
            if not re.search(class_pattern, content):
                continue
            
            # Extract schema from the class
            return self._extract_schema_from_content(content)
        
        return None
    
    def _extract_schema_from_content(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract OpenAPI schema from Java class content."""
        properties = {}
        required = []
        
        # Pattern to match field declarations: private Type fieldName;
        # or: private Type fieldName = defaultValue;
        # Handle both single-line and multi-line declarations
        # Also support protected and package-private fields
        field_pattern = r'(?:private|protected)\s+([\w<>[\],\s]+)\s+(\w+)(?:\s*=\s*[^;]+)?\s*;'
        
        for match in re.finditer(field_pattern, content, re.MULTILINE):
            field_type = match.group(1).strip()
            field_name = match.group(2).strip()
            
            # Skip if it's a method (has parentheses) or if field_name looks like a method
            if '(' in field_type or ')' in field_type:
                continue
            
            # Convert Java type to OpenAPI type
            openapi_type = self._java_type_to_openapi_type(field_type)
            
            # Check if field has a default value (making it optional)
            field_declaration = match.group(0)
            has_default = '=' in field_declaration
            
            if not has_default:
                required.append(field_name)
            
            properties[field_name] = {
                "type": openapi_type,
            }
        
        if properties:
            schema = {
                "type": "object",
                "properties": properties,
            }
            if required:
                schema["required"] = required
            return schema
        
        return None

    def _resolve_constant(self, class_name: str, constant_name: str, current_file: Path) -> Optional[str]:
        """
        Resolve a constant value from a class.
        
        Args:
            class_name: Name of the class containing the constant (e.g., "BaseController")
            constant_name: Name of the constant (e.g., "PROJECTS_BASE")
            current_file: Path to the current file (for relative imports)
            
        Returns:
            Resolved constant value or None if not found
        """
        # Try to find the class file
        class_file = self._find_class_file(class_name, current_file)
        if not class_file:
            return None
        
        # Read the class file
        class_content = self.read_file(class_file)
        if not class_content:
            return None
        
        # Extract constant value
        # Pattern: public static final String CONSTANT_NAME = "value";
        # Or: public static final String CONSTANT_NAME = OTHER_CONSTANT + "/path";
        constant_pattern = rf'public\s+static\s+final\s+String\s+{constant_name}\s*=\s*([^;]+);'
        match = re.search(constant_pattern, class_content)
        if not match:
            return None
        
        constant_value_expr = match.group(1).strip()
        
        # Handle string literals: "value"
        if constant_value_expr.startswith('"') and constant_value_expr.endswith('"'):
            return constant_value_expr.strip('"')
        
        # Handle string concatenation: CONSTANT1 + "/path" or "path" + CONSTANT2
        parts = []
        # Split by + and process each part
        concat_parts = re.split(r'\s*\+\s*', constant_value_expr)
        for part in concat_parts:
            part = part.strip()
            # String literal
            if part.startswith('"') and part.endswith('"'):
                parts.append(part.strip('"'))
            # Another constant reference
            elif '.' in part:
                # Format: ClassName.CONSTANT_NAME
                const_match = re.match(r'(\w+)\.(\w+)', part)
                if const_match:
                    const_class = const_match.group(1)
                    const_name = const_match.group(2)
                    # Recursively resolve
                    resolved = self._resolve_constant(const_class, const_name, class_file)
                    if resolved:
                        parts.append(resolved)
                    else:
                        return None  # Can't resolve dependency
                else:
                    return None  # Invalid format
            else:
                # Might be a simple constant name in the same class
                same_class_match = re.search(
                    rf'public\s+static\s+final\s+String\s+{part}\s*=\s*"([^"]+)"',
                    class_content
                )
                if same_class_match:
                    parts.append(same_class_match.group(1))
                else:
                    return None  # Can't resolve
        
        return ''.join(parts)
    
    def _find_class_file(self, class_name: str, reference_file: Path) -> Optional[Path]:
        """
        Find the file containing a class definition.
        
        Args:
            class_name: Name of the class to find
            reference_file: File that references this class (for package resolution)
            
        Returns:
            Path to the class file or None if not found
        """
        # Try to find in cached files first
        for file_path, content in self._file_content_cache.items():
            # Check if file contains the class definition
            class_pattern = rf'(?:public\s+)?(?:abstract\s+)?(?:class|interface|enum)\s+{class_name}\b'
            if re.search(class_pattern, content):
                return file_path
        
        # Try to find by filename (common convention: ClassName.java)
        for file_path in self.source_paths:
            if file_path.name == f"{class_name}.java":
                return file_path
        
        # Try to find in same package (extract package from reference file)
        try:
            ref_content = self.read_file(reference_file)
            if ref_content:
                package_match = re.search(r'package\s+([\w.]+);', ref_content)
                if package_match:
                    package = package_match.group(1)
                    # Search for class in same package directory
                    ref_dir = reference_file.parent
                    candidate = ref_dir / f"{class_name}.java"
                    if candidate.exists():
                        return candidate
        except:
            pass
        
        # Search all Java files
        for file_path in self.find_files("*.java"):
            try:
                content = self.read_file(file_path)
                if content:
                    class_pattern = rf'(?:public\s+)?(?:abstract\s+)?(?:class|interface|enum)\s+{class_name}\b'
                    if re.search(class_pattern, content):
                        return file_path
            except:
                continue
        
        return None
    
    def _extract_inherited_request_mapping(self, content: str, file_path: Path) -> Optional[str]:
        """
        Extract @RequestMapping from a base class if the controller extends it.
        
        Args:
            content: Controller file content
            file_path: Path to controller file
            
        Returns:
            Base class @RequestMapping path or None
        """
        # Check if class extends another class
        extends_match = re.search(r'class\s+\w+\s+extends\s+(\w+)', content)
        if not extends_match:
            return None
        
        base_class_name = extends_match.group(1)
        base_class_file = self._find_class_file(base_class_name, file_path)
        
        if base_class_file:
            base_content = self.read_file(base_class_file)
            if base_content:
                # Extract @RequestMapping from base class
                base_path = self._extract_class_request_mapping(base_content, base_class_file)
                if base_path:
                    return base_path
        
        return None

    def _extract_controller_name(self, content: str, file_path: Path) -> str:
        """Extract controller class name from file content or file path."""
        # Try to extract from class declaration first
        class_match = re.search(r'public\s+class\s+(\w+)', content)
        if class_match:
            class_name = class_match.group(1)
            # Remove common suffixes for cleaner tag names
            for suffix in ['Controller', 'Resource', 'Endpoint', 'Api']:
                if class_name.endswith(suffix):
                    return class_name[:-len(suffix)]
            return class_name
        
        # Fallback to file name
        file_name = file_path.stem  # Gets filename without extension
        # Remove common suffixes
        for suffix in ['Controller', 'Resource', 'Endpoint', 'Api']:
            if file_name.endswith(suffix):
                return file_name[:-len(suffix)]
        return file_name
    
    def _generate_operation_id(
        self, 
        path: str, 
        method: HTTPMethod, 
        controller_name: Optional[str] = None,
        method_name: Optional[str] = None,
    ) -> str:
        """Generate unique operation ID from path, method, controller, and method name."""
        # Build operation ID components
        parts = []
        
        # Start with HTTP method
        parts.append(method.value.lower())
        
        # Add controller name if available (makes it unique)
        if controller_name:
            # Convert to camelCase: "PrimaryTransaction" -> "primaryTransaction"
            controller_camel = controller_name[0].lower() + controller_name[1:] if controller_name else ""
            parts.append(controller_camel)
        
        # Add method name if available (further uniqueness)
        if method_name:
            parts.append(method_name)
        
        # Add path parts as fallback if no method name
        if not method_name:
            path_parts = [p for p in path.split('/') if p and not p.startswith('{')]
            parts.extend(p.capitalize() for p in path_parts)
        
        # Join parts: e.g., "getPrimaryTransactionGetById"
        operation_id = ''.join(parts)
        
        # If still empty or too generic, use path-based fallback
        if not operation_id or operation_id == method.value.lower():
            path_parts = [p for p in path.split('/') if p and not p.startswith('{')]
            if path_parts:
                operation_id = method.value.lower() + ''.join(p.capitalize() for p in path_parts)
            else:
                operation_id = method.value.lower() + "Endpoint"
        
        return operation_id

