"""ASP.NET Core endpoint enricher."""

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


class DotNetEnricher(BaseEnricher):
    """Enricher for ASP.NET Core endpoints."""

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.ASPNET_CORE

    def enrich_endpoint(self, endpoint: APIEndpoint, content: str) -> APIEndpoint:
        """Enrich ASP.NET Core endpoint."""
        # Find the method signature
        method_signature = self._find_method(content, endpoint.path, endpoint.method)
        if not method_signature:
            return endpoint

        # Only extract request body if it doesn't already exist or is generic
        # The parser should have already extracted it correctly with full schemas
        if not endpoint.request_body or self._is_generic_schema(endpoint.request_body):
            request_body = self._extract_request_body(method_signature, content)
            if request_body:
                endpoint.request_body = request_body

        # Enhance parameters
        enhanced_params = self._extract_parameters(method_signature, endpoint.path, content)
        if enhanced_params:
            endpoint.parameters = self._merge_parameters(
                endpoint.parameters, enhanced_params
            )

        return endpoint
    
    def _is_generic_schema(self, request_body: Dict[str, Any]) -> bool:
        """Check if request body schema is generic (just type: object with no properties)."""
        try:
            schema = request_body.get("content", {}).get("application/json", {}).get("schema", {})
            if schema.get("type") == "object" and "properties" not in schema:
                return True
        except (AttributeError, KeyError, TypeError):
            pass
        return False

    def _find_method(
        self, content: str, path: str, method: HTTPMethod
    ) -> Optional[str]:
        """Find ASP.NET Core method signature."""
        annotation_map = {
            HTTPMethod.GET: "HttpGet",
            HTTPMethod.POST: "HttpPost",
            HTTPMethod.PUT: "HttpPut",
            HTTPMethod.DELETE: "HttpDelete",
            HTTPMethod.PATCH: "HttpPatch",
        }

        annotation = annotation_map.get(method, "HttpGet")
        pattern = rf'\[{annotation}[^\]]*\]'
        match = re.search(pattern, content)
        if match:
            start = match.end()
            method_pattern = r'(public|private|protected)?\s+[\w<>[\],\s]+\s+\w+\s*\([^)]*\)'
            method_match = re.search(method_pattern, content[start : start + 500])
            if method_match:
                return method_match.group(0)

        return None

    def _extract_request_body(
        self, signature: str, content: str
    ) -> Optional[Dict[str, Any]]:
        """Extract request body from ASP.NET Core method."""
        if "[FromBody]" not in signature:
            return None

        pattern = r'\[FromBody\]\s+([\w<>[\],\s]+)\s+\w+'
        match = re.search(pattern, signature)
        if match:
            param_type = match.group(1).strip()
            schema = self._csharp_type_to_schema(param_type)
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
        """Extract detailed parameters from ASP.NET Core method."""
        parameters = []

        path_vars = self._extract_path_variables(path)
        for var in path_vars:
            pattern = rf'\[FromRoute\]\s+([\w<>[\],\s]+)\s+{var}'
            match = re.search(pattern, signature)
            param_type = "string"
            if match:
                param_type = self._csharp_type_to_openapi_type(match.group(1).strip())

            parameters.append(
                APIParameter(
                    name=var,
                    location=ParameterLocation.PATH,
                    required=True,
                    type=param_type,
                )
            )

        # Extract [FromQuery] parameters
        pattern = r'\[FromQuery\]\s+([\w<>[\],\s]+)\s+(\w+)'
        for match in re.finditer(pattern, signature):
            param_type = self._csharp_type_to_openapi_type(match.group(1).strip())
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

        return parameters

    def _extract_path_variables(self, path: str) -> List[str]:
        """Extract path variables from path string."""
        pattern = r'\{(\w+)\}'
        return re.findall(pattern, path)

    def _csharp_type_to_openapi_type(self, csharp_type: str) -> str:
        """Convert C# type to OpenAPI type."""
        csharp_type = csharp_type.strip()
        type_map = {
            "int": "integer",
            "Int32": "integer",
            "long": "integer",
            "Int64": "integer",
            "float": "number",
            "Float": "number",
            "double": "number",
            "Double": "number",
            "bool": "boolean",
            "Boolean": "boolean",
            "string": "string",
            "String": "string",
            "char": "string",
            "Char": "string",
        }
        return type_map.get(csharp_type, "string")

    def _csharp_type_to_schema(self, csharp_type: str) -> Dict[str, Any]:
        """Convert C# type to OpenAPI schema."""
        csharp_type = csharp_type.strip()

        if "<" in csharp_type:
            base_type = csharp_type.split("<")[0].strip()
            if base_type in ["List", "IList", "ICollection", "IEnumerable"]:
                return {"type": "array", "items": {"type": "string"}}
            elif base_type in ["Dictionary", "IDictionary"]:
                return {"type": "object", "additionalProperties": True}

        openapi_type = self._csharp_type_to_openapi_type(csharp_type)
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

