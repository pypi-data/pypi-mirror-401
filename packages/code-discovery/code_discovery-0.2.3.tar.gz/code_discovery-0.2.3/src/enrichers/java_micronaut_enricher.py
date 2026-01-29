"""Micronaut endpoint enricher."""

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


class MicronautEnricher(BaseEnricher):
    """Enricher for Micronaut endpoints."""

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.MICRONAUT

    def enrich_endpoint(self, endpoint: APIEndpoint, content: str) -> APIEndpoint:
        """Enrich Micronaut endpoint."""
        # Find the method signature for this endpoint
        method_signature = self._find_method(content, endpoint.path, endpoint.method)
        if not method_signature:
            return endpoint

        # Extract request body
        request_body = self._extract_request_body(method_signature, content)
        if request_body:
            endpoint.request_body = request_body

        # Enhance parameters
        enhanced_params = self._extract_parameters(method_signature, endpoint.path, content)
        if enhanced_params:
            endpoint.parameters = self._merge_parameters(
                endpoint.parameters, enhanced_params
            )

        # Extract response schema
        response_schema = self._extract_response(method_signature, content)
        if response_schema and endpoint.responses:
            endpoint.responses[0].schema = response_schema

        return endpoint

    def _find_method(
        self, content: str, path: str, method: HTTPMethod
    ) -> Optional[str]:
        """Find Micronaut method signature."""
        annotation_map = {
            HTTPMethod.GET: "@Get",
            HTTPMethod.POST: "@Post",
            HTTPMethod.PUT: "@Put",
            HTTPMethod.DELETE: "@Delete",
            HTTPMethod.PATCH: "@Patch",
        }

        annotation = annotation_map.get(method, "@Get")
        
        path_segments = [s for s in path.split("/") if s and not s.startswith("{")]
        if path_segments:
            path_pattern = re.escape(path_segments[-1])
        else:
            path_pattern = ""

        if path_pattern:
            pattern = rf'{annotation}\s*\([^)]*["\']?{path_pattern}["\']?[^)]*\)'
            match = re.search(pattern, content)
            if match:
                start = match.end()
                method_pattern = r'(public|private|protected)?\s+[\w<>[\],\s]+\s+\w+\s*\([^)]*\)'
                method_match = re.search(method_pattern, content[start : start + 500])
                if method_match:
                    return method_match.group(0)

        pattern = rf'{annotation}\s*\([^)]*\)'
        matches = list(re.finditer(pattern, content))
        if matches:
            match = matches[0]
            start = match.end()
            method_pattern = r'(public|private|protected)?\s+[\w<>[\],\s]+\s+\w+\s*\([^)]*\)'
            method_match = re.search(method_pattern, content[start : start + 500])
            if method_match:
                return method_match.group(0)

        return None

    def _extract_request_body(
        self, signature: str, content: str
    ) -> Optional[Dict[str, Any]]:
        """Extract request body from Micronaut method."""
        if "@Body" not in signature:
            return None

        pattern = r'@Body\s+(?:@\w+\s+)*(?:final\s+)?([\w<>[\],\s]+)\s+\w+'
        match = re.search(pattern, signature)
        if match:
            param_type = match.group(1).strip()
            schema = self._java_type_to_schema(param_type)
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
        """Extract detailed parameters from Micronaut method."""
        parameters = []

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

        # Extract @QueryValue parameters
        pattern = r'@QueryValue\s*(?:\([^)]*\))?\s+(?:final\s+)?([\w<>[\],\s]+)\s+(\w+)'
        for match in re.finditer(pattern, signature):
            param_type = self._java_type_to_openapi_type(match.group(1).strip())
            param_name = match.group(2)
            if param_name not in path_vars:
                parameters.append(
                    APIParameter(
                        name=param_name,
                        location=ParameterLocation.QUERY,
                        required=False,
                        type=param_type,
                    )
                )

        # Extract @Header parameters
        pattern = r'@Header\s*(?:\([^)]*\))?\s+(?:final\s+)?([\w<>[\],\s]+)\s+(\w+)'
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
        self, signature: str, content: str
    ) -> Optional[Dict[str, Any]]:
        """Extract response schema from Micronaut method return type."""
        pattern = r'public\s+([\w<>[\],\s]+)\s+\w+\s*\('
        match = re.search(pattern, signature)
        if match:
            return_type = match.group(1).strip()
            if return_type in ["void", "Void"]:
                return None
            return self._java_type_to_schema(return_type)
        return None

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

    def _java_type_to_schema(self, java_type: str) -> Dict[str, Any]:
        """Convert Java type to OpenAPI schema."""
        java_type = java_type.strip()

        if "<" in java_type:
            base_type = java_type.split("<")[0].strip()
            if base_type in ["List", "ArrayList", "Set", "HashSet"]:
                return {"type": "array", "items": {"type": "string"}}
            elif base_type in ["Map", "HashMap"]:
                return {"type": "object", "additionalProperties": True}

        openapi_type = self._java_type_to_openapi_type(java_type)
        if openapi_type != "string":
            return {"type": openapi_type}

        return {"type": "object"}

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

