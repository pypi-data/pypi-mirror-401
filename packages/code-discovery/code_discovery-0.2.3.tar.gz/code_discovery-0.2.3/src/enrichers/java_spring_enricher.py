"""Spring Boot endpoint enricher."""

import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from enrichers.base import BaseEnricher
from core.models import (
    APIEndpoint,
    APIParameter,
    FrameworkType,
    HTTPMethod,
    ParameterLocation,
)


class SpringBootEnricher(BaseEnricher):
    """Enricher for Spring Boot endpoints."""

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.SPRING_BOOT

    def enrich_endpoint(self, endpoint: APIEndpoint, content: str) -> APIEndpoint:
        """Enrich Spring Boot endpoint."""
        # Find the method signature for this endpoint
        method_signature = self._find_method(content, endpoint.path, endpoint.method)
        if not method_signature:
            return endpoint

        # Extract request body (only if not already set or if we can improve it)
        request_body = self._extract_request_body(method_signature, content, endpoint.source_file)
        if request_body:
            # Only override if current request body is generic or missing
            if not endpoint.request_body or self._is_generic_schema(endpoint.request_body):
                endpoint.request_body = request_body

        # Enhance parameters with types and required flags
        enhanced_params = self._extract_parameters(method_signature, endpoint.path, content)
        if enhanced_params:
            # Merge with existing parameters
            endpoint.parameters = self._merge_parameters(
                endpoint.parameters, enhanced_params
            )

        # Extract response schema (always try to enhance, even if parser set one)
        response_schema = self._extract_response(method_signature, content, endpoint.source_file)
        if response_schema and endpoint.responses:
            # Always override if we found a better schema (not generic)
            if not self._is_generic_schema(response_schema):
                endpoint.responses[0].schema = response_schema
            elif not endpoint.responses[0].schema or self._is_generic_schema(endpoint.responses[0].schema):
                # Even if generic, use it if we don't have one or current is also generic
                endpoint.responses[0].schema = response_schema

        return endpoint

    def _is_generic_schema(self, schema: Any) -> bool:
        """Check if schema is just a generic object without properties."""
        if isinstance(schema, dict):
            # Generic object without properties
            if schema.get("type") == "object" and "properties" not in schema:
                return True
        return False

    def _find_method(
        self, content: str, path: str, method: HTTPMethod
    ) -> Optional[str]:
        """Find Spring Boot method signature."""
        # Map HTTP method to annotation
        annotation_map = {
            HTTPMethod.GET: "@GetMapping",
            HTTPMethod.POST: "@PostMapping",
            HTTPMethod.PUT: "@PutMapping",
            HTTPMethod.DELETE: "@DeleteMapping",
            HTTPMethod.PATCH: "@PatchMapping",
        }

        annotation = annotation_map.get(method, "@RequestMapping")
        
        # Try to find annotation with matching path
        path_segments = [s for s in path.split("/") if s and not s.startswith("{")]
        if path_segments:
            path_pattern = re.escape(path_segments[-1])
        else:
            path_pattern = ""

        # Find annotation with matching path
        if path_pattern:
            pattern = rf'{annotation}\s*\([^)]*["\']?{path_pattern}["\']?[^)]*\)'
            match = re.search(pattern, content)
            if match:
                start = match.end()
                method_signature = self._extract_full_method_signature(content, start)
                if method_signature:
                    return method_signature

        # Fallback: find any method with the annotation
        pattern = rf'{annotation}\s*\([^)]*\)'
        matches = list(re.finditer(pattern, content))
        if matches:
            match = matches[0]
            start = match.end()
            method_signature = self._extract_full_method_signature(content, start)
            if method_signature:
                return method_signature

        return None

    def _extract_full_method_signature(self, content: str, start_pos: int) -> Optional[str]:
        """Extract full Java method signature, handling multi-line parameters."""
        remaining = content[start_pos:]
        
        # Find method visibility modifier
        visibility_match = re.search(r'^(public|private|protected)\s+', remaining)
        if visibility_match:
            method_start_idx = visibility_match.start()
            after_visibility = visibility_match.end()
        else:
            method_start_idx = 0
            after_visibility = 0
        
        # Find the method name - it's the last identifier before the opening paren
        # This handles nested generics in return types
        method_name_pattern = r'(\w+)\s*\('
        method_name_match = re.search(method_name_pattern, remaining[after_visibility:])
        if not method_name_match:
            return None
        
        # The opening paren is at after_visibility + method_name_match.end() - 1
        paren_start = after_visibility + method_name_match.end() - 1
        
        # Find matching closing parenthesis
        paren_count = 0
        i = paren_start
        in_string = False
        string_char = None
        
        while i < len(remaining) and i < paren_start + 2000:
            char = remaining[i]
            
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
                        return remaining[method_start_idx:i + 1]
            i += 1
        
        return None

    def _extract_request_body(
        self, signature: str, content: str, source_file: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Extract request body from Spring Boot method."""
        if "@RequestBody" not in signature:
            return None

        pattern = r'@RequestBody\s+(?:@\w+\s+)*(?:final\s+)?([\w<>[\],\s]+)\s+\w+'
        match = re.search(pattern, signature, re.MULTILINE | re.DOTALL)
        if match:
            param_type = match.group(1).strip()
            # Get file path for model parsing
            file_path = None
            if source_file:
                file_path = self.repo_path / source_file
                if not file_path.exists():
                    file_path = None
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

    def _extract_parameters(
        self, signature: str, path: str, content: str
    ) -> List[APIParameter]:
        """Extract detailed parameters from Spring Boot method."""
        parameters = []

        # Extract path variables
        path_vars = self._extract_path_variables(path)
        for var in path_vars:
            pattern = rf'@PathVariable\s*\([^)]*["\']?{var}["\']?[^)]*\)\s+(?:final\s+)?([\w<>[\],\s]+)\s+\w+'
            match = re.search(pattern, signature)
            param_type = "string"
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

        # Extract @RequestParam parameters
        pattern = r'@RequestParam\s*(?:\([^)]*\))?\s+(?:final\s+)?([\w<>[\],\s]+)\s+(\w+)'
        for match in re.finditer(pattern, signature):
            param_type = self._java_type_to_openapi_type(match.group(1).strip())
            param_name = match.group(2)
            if param_name not in path_vars:
                required = "required" not in match.group(0) or "required=true" in match.group(0)
                parameters.append(
                    APIParameter(
                        name=param_name,
                        location=ParameterLocation.QUERY,
                        required=required,
                        type=param_type,
                    )
                )

        # Extract @RequestHeader parameters
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

    def _extract_response(
        self, signature: str, content: str, source_file: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Extract response schema from Spring Boot method return type."""
        # Extract return type - need to capture full type including nested generics
        # Method signature format: [visibility] ReturnType methodName(params)
        
        # Find visibility modifier (optional)
        visibility_match = re.search(r'^(public|private|protected)\s+', signature)
        if visibility_match:
            start_pos = visibility_match.end()
        else:
            start_pos = 0
        
        # Find the opening parenthesis of the method parameters
        paren_pos = signature.find('(')
        if paren_pos == -1:
            return None
        
        # Extract everything from start_pos to paren_pos
        return_and_method = signature[start_pos:paren_pos].strip()
        
        # Find the last word (method name) - it's the last identifier before the paren
        method_name_match = re.search(r'(\w+)\s*$', return_and_method)
        if not method_name_match:
            return None
        
        method_name_start = method_name_match.start()
        return_type = return_and_method[:method_name_start].strip()
        
        if return_type in ["void", "Void", "HttpStatus"] or not return_type:
            return None
        
        # Get file path for model parsing
        file_path = None
        if source_file:
            file_path = self.repo_path / source_file
            if not file_path.exists():
                file_path = None
        
        return self._java_type_to_schema(return_type, file_path)

    def _extract_path_variables(self, path: str) -> List[str]:
        """Extract path variables from path string."""
        pattern = r'\{(\w+)\}'
        return re.findall(pattern, path)

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
            # Extract base type
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

        return {"type": "object"}

    def _parse_java_model(self, class_name: str, controller_file: Optional[Path] = None) -> Optional[Dict[str, Any]]:
        """Parse a Java model class to extract field definitions."""
        # Search for the model class file in the repository
        # Use self.repo_path directly for searching
        repo_root = self.repo_path
        
        # Search for Java files in common source directories
        search_paths = [
            repo_root / "src" / "main" / "java",
            repo_root / "src" / "test" / "java",
        ]
        
        java_files = []
        for search_path in search_paths:
            if search_path.exists():
                java_files.extend(search_path.rglob("*.java"))
        
        # If no files found in standard locations, search entire repo
        if not java_files:
            java_files = list(repo_root.rglob("*.java"))
        
        for java_file in java_files:
            # Skip controller files
            if "controller" in str(java_file).lower() or "Controller" in java_file.name:
                continue
            
            try:
                content = self.read_file(java_file)
                if not content:
                    continue
                
                # Check if this file contains the class we're looking for
                class_pattern = rf'public\s+class\s+{re.escape(class_name)}\b'
                if not re.search(class_pattern, content):
                    continue
                
                # Extract fields from the class
                properties = {}
                required = []
                
                # Pattern to match field declarations
                field_pattern = r'private\s+([\w<>[\],\s]+)\s+(\w+)(?:\s*=\s*[^;]+)?\s*;'
                
                for match in re.finditer(field_pattern, content, re.MULTILINE):
                    field_type = match.group(1).strip()
                    field_name = match.group(2).strip()
                    
                    # Skip if it's a method
                    if '(' in field_type or ')' in field_type:
                        continue
                    
                    # Convert Java type to OpenAPI type
                    openapi_type = self._java_type_to_openapi_type(field_type)
                    
                    # Check if field has a default value
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
            except Exception:
                continue
        
        return None

    def _merge_parameters(
        self, existing: List[APIParameter], new_params: List[APIParameter]
    ) -> List[APIParameter]:
        """Merge parameter lists, preferring new parameters when names match."""
        merged = []
        existing_names = {p.name: p for p in existing}

        for new_param in new_params:
            if new_param.name in existing_names:
                merged.append(new_param)
                del existing_names[new_param.name]
            else:
                merged.append(new_param)

        for param in existing_names.values():
            merged.append(param)

        return merged

