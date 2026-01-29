"""ASP.NET Core parser."""

import re
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from parsers.base import BaseParser
from core.models import (
    APIEndpoint,
    APIParameter,
    APIResponse,
    DiscoveryResult,
    FrameworkType,
    HTTPMethod,
    ParameterLocation,
)


class DotNetParser(BaseParser):
    """Parser for ASP.NET Core APIs."""

    SIMPLE_TYPES = {
        "string",
        "String",
        "int",
        "Int32",
        "long",
        "Int64",
        "float",
        "Float",
        "double",
        "Double",
        "decimal",
        "Decimal",
        "bool",
        "Boolean",
        "Guid",
        "DateTime",
        "DateOnly",
        "TimeOnly",
    }

    SERVICE_TYPES = {
        "ILogger",
        "ILoggerFactory",
        "IServiceProvider",
        "CancellationToken",
        "ISender",
        "IMediator",
        "IMapper",
        "HttpContext",
        "HttpRequest",
        "HttpResponse",
        "IHttpClientFactory",
        "IOptions",
        "IConfiguration",
    }

    def __init__(self, source_paths: List[Path], repo_path: Path):
        super().__init__(source_paths, repo_path)
        self._type_schema_cache: Dict[str, Dict[str, Any]] = {}
        self._file_content_cache: Dict[Path, str] = {}

    def parse(self) -> DiscoveryResult:
        """Parse ASP.NET Core source files for API endpoints."""
        endpoints: List[APIEndpoint] = []
        cs_files = self.find_files("*.cs")

        # First pass: cache all file contents for cross-file type resolution
        for cs_file in cs_files:
            content = self.read_file(cs_file)
            if content:
                self._file_content_cache[cs_file] = content

        # Second pass: parse endpoints (now with full type cache available)
        for cs_file in cs_files:
            content = self._file_content_cache.get(cs_file)
            if not content:
                continue

            if self._is_api_controller(content):
                endpoints.extend(self._parse_controller(cs_file, content))

            if self._is_carter_module(content):
                endpoints.extend(self._parse_carter_module(cs_file, content))

        return DiscoveryResult(
            framework=FrameworkType.ASPNET_CORE,
            endpoints=endpoints,
            title="ASP.NET Core API",
        )

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.ASPNET_CORE

    def _is_api_controller(self, content: str) -> bool:
        """Check if the class is an API controller (ASP.NET Core or ASP.NET MVC Framework)."""
        # ASP.NET Core patterns
        if "[ApiController]" in content or ": ControllerBase" in content:
            return True
        
        # ASP.NET MVC Framework patterns
        # Check for inheritance from Controller (not ControllerBase)
        if re.search(r':\s*Controller\b', content):
            # Also check if it has HTTP method attributes or Route attributes
            if any(pattern in content for pattern in [
                "[HttpGet", "[HttpPost", "[HttpPut", "[HttpDelete", "[HttpPatch",
                "[Route(", "[ActionName(",
            ]):
                return True
        
        # Check for System.Web.Mvc namespace (ASP.NET MVC Framework)
        if "System.Web.Mvc" in content and ": Controller" in content:
            return True
        
        return False

    def _parse_controller(self, file_path: Path, content: str) -> List[APIEndpoint]:
        """Parse a controller file for endpoints."""
        endpoints = []
        
        # Extract class-level [Route] attribute
        class_route = self._extract_class_route(content)
        
        # Find all HTTP method attributes
        methods = self._extract_methods(content)
        
        for method_info in methods:
            endpoint = self._create_endpoint(
                method_info,
                class_route,
                file_path,
                content,
            )
            if endpoint:
                endpoints.append(endpoint)

        return endpoints

    def _extract_class_route(self, content: str) -> str:
        """Extract class-level [Route] attribute (ASP.NET Core and MVC Framework)."""
        # Find the class declaration first
        class_match = re.search(r'class\s+(\w+)Controller', content)
        if not class_match:
            return ""
        
        class_start = class_match.start()
        # Find the opening brace of the class
        class_brace = content.find('{', class_start)
        if class_brace == -1:
            return ""
        
        # Only search for route attributes before the class opening brace
        class_declaration = content[:class_brace]
        
        # Match [Route("path")] or [Route("api/[controller]")] before class
        patterns = [
            (r'\[Route\s*\(\s*"([^"]+)"\s*\)\]', 1),
            (r'\[RoutePrefix\s*\(\s*"([^"]+)"\s*\)\]', 1),  # ASP.NET MVC Framework
        ]
        
        for pattern, group_num in patterns:
            # Search in reverse to get the last match before the class
            matches = list(re.finditer(pattern, class_declaration))
            if matches:
                # Get the last match (closest to the class declaration)
                match = matches[-1]
                route = match.group(group_num)
                # Handle [controller] placeholder
                if '[controller]' in route:
                    controller_name = class_match.group(1).lower()
                    route = route.replace('[controller]', controller_name)
                return route
        
        # For ASP.NET MVC Framework, if no explicit route, use convention-based routing
        # Check if this is MVC Framework (has System.Web.Mvc)
        if "System.Web.Mvc" in content:
            controller_name = class_match.group(1).lower()
            # Convention: /ControllerName (without "Controller" suffix)
            return controller_name
        
        return ""

    def _extract_methods(self, content: str) -> List[Dict[str, Any]]:
        """Extract method information from controller (ASP.NET Core and MVC Framework)."""
        methods = []
        
        # Patterns for HTTP attributes (both Core and Framework)
        http_patterns = [
            (r'\[HttpGet\s*\(\s*"([^"]+)"\s*\)\]', HTTPMethod.GET),
            (r'\[HttpGet\]', HTTPMethod.GET),
            (r'\[HttpPost\s*\(\s*"([^"]+)"\s*\)\]', HTTPMethod.POST),
            (r'\[HttpPost\]', HTTPMethod.POST),
            (r'\[HttpPut\s*\(\s*"([^"]+)"\s*\)\]', HTTPMethod.PUT),
            (r'\[HttpPut\]', HTTPMethod.PUT),
            (r'\[HttpDelete\s*\(\s*"([^"]+)"\s*\)\]', HTTPMethod.DELETE),
            (r'\[HttpDelete\]', HTTPMethod.DELETE),
            (r'\[HttpPatch\s*\(\s*"([^"]+)"\s*\)\]', HTTPMethod.PATCH),
            (r'\[HttpPatch\]', HTTPMethod.PATCH),
        ]
        
        # Track which methods have been found with attributes
        found_methods = set()
        
        for pattern, http_method in http_patterns:
            for match in re.finditer(pattern, content):
                # Extract path if present in the HTTP attribute
                path = match.group(1) if match.lastindex and match.lastindex >= 1 else ""
                
                # Extract method signature
                method_start = match.end()
                method_signature = self._extract_method_signature(content, method_start)
                
                # If no path in HTTP attribute, check for separate [Route] attribute
                if not path:
                    # Look for [Route("path")] between HTTP attribute and method signature
                    # Search in a reasonable window (up to 200 chars after the attribute)
                    search_end = min(method_start + 200, len(content))
                    search_section = content[method_start:search_end]
                    route_match = re.search(r'\[Route\s*\(\s*"([^"]*)"\s*\)\]', search_section)
                    if route_match:
                        path = route_match.group(1)  # Can be empty string ""
                
                # If still no path specified (and Route wasn't empty), use method name
                if path is None and method_signature:
                    method_name = self._extract_method_name(method_signature)
                    if method_name:
                        path = method_name
                        # Check for [ActionName] attribute override
                        action_name = self._extract_action_name(content, method_start)
                        if action_name:
                            path = action_name
                
                methods.append({
                    "path": path,
                    "method": http_method,
                    "signature": method_signature,
                    "position": match.start(),
                })
                found_methods.add(method_start)
        
        # For ASP.NET MVC Framework: also check for convention-based routing
        # If no explicit HTTP attributes, look for public methods that return ActionResult
        if "System.Web.Mvc" in content and not found_methods:
            # Find public methods that might be action methods
            public_method_pattern = r'public\s+(?:async\s+)?(?:ActionResult|JsonResult|ViewResult|ContentResult|RedirectResult|HttpStatusCodeResult|object|string|int|void)\s+(\w+)\s*\('
            for match in re.finditer(public_method_pattern, content):
                method_name = match.group(1)
                # Skip special methods
                if method_name in ['GetType', 'ToString', 'Equals', 'GetHashCode', 'Dispose']:
                    continue
                # Default to GET for convention-based routing
                methods.append({
                    "path": method_name,
                    "method": HTTPMethod.GET,
                    "signature": match.group(0),
                    "position": match.start(),
                })
        
        return methods
    
    def _extract_route_attribute(self, content: str, attr_start: int, method_start: int) -> Optional[str]:
        """Extract [Route] attribute value between HTTP attribute and method signature."""
        # Look for [Route("path")] in the section between attributes
        section = content[attr_start:method_start]
        route_match = re.search(r'\[Route\s*\(\s*"([^"]+)"\s*\)\]', section)
        if route_match:
            return route_match.group(1)
        return None
    
    def _extract_action_name(self, content: str, method_start: int) -> Optional[str]:
        """Extract [ActionName] attribute value for ASP.NET MVC Framework."""
        # Look backwards from method start for [ActionName("name")]
        before_method = content[:method_start]
        action_name_match = re.search(r'\[ActionName\s*\(\s*"([^"]+)"\s*\)\]', before_method)
        if action_name_match:
            return action_name_match.group(1)
        return None

    def _extract_method_signature(self, content: str, start_pos: int) -> str:
        """Extract C# method signature after attribute."""
        # Match method declaration
        method_pattern = r'\s*(?:public|private|protected|internal)?\s+[^\(\)]+\s+\w+\s*\([^)]*\)'
        match = re.search(method_pattern, content[start_pos:start_pos+500])
        if match:
            return match.group(0)
        return ""

    def _extract_method_name(self, signature: str) -> str:
        """Extract method name from signature."""
        match = re.search(r'\s+(\w+)\s*\(', signature)
        if match:
            return match.group(1)
        return ""

    def _create_endpoint(
        self,
        method_info: Dict[str, Any],
        class_route: str,
        file_path: Path,
        file_content: str,
    ) -> Optional[APIEndpoint]:
        """Create an APIEndpoint from method information."""
        # Combine class route and method path
        full_path = self._combine_paths(class_route, method_info["path"])
        full_path = self.normalize_path(full_path)
        
        # Extract parameters from signature
        parameters = self._extract_parameters(method_info["signature"], full_path)
        
        # Extract request body (only for methods that support it)
        request_body = None
        if method_info["method"] not in {HTTPMethod.GET, HTTPMethod.HEAD, HTTPMethod.OPTIONS, HTTPMethod.DELETE}:
            request_body = self._extract_request_body(method_info["signature"], file_content)
        
        # Extract response schema
        response_schema = self._extract_response_schema(method_info["signature"], file_content)
        
        # Create endpoint
        endpoint = APIEndpoint(
            path=full_path,
            method=method_info["method"],
            operation_id=self._generate_operation_id(full_path, method_info["method"]),
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
            source_line=self._calculate_line_number(file_content, method_info.get("position", 0)),
        )
        
        return endpoint

    def _is_carter_module(self, content: str) -> bool:
        """Check if file contains Carter minimal API modules."""
        return "ICarterModule" in content or "MapGet(" in content or "MapPost(" in content

    def _parse_carter_module(self, file_path: Path, content: str) -> List[APIEndpoint]:
        """Parse Carter minimal APIs (and general Map* routes)."""
        endpoints: List[APIEndpoint] = []

        for route in self._extract_carter_routes(content):
            normalized_path = self.normalize_path(route["path"])
            parameters = self._create_path_parameters(normalized_path)
            extra_params, request_body = self._classify_lambda_parameters(
                route.get("lambda_params", []),
                normalized_path,
                content,
                parameters,
            )
            parameters.extend(extra_params)

            responses = route.get("responses") or [
                APIResponse(
                    status_code=200,
                    description="Successful response",
                )
            ]

            # GET, HEAD, and OPTIONS methods should not have requestBody
            final_request_body = None
            if route["method"] not in {HTTPMethod.GET, HTTPMethod.HEAD, HTTPMethod.OPTIONS}:
                final_request_body = request_body

            endpoint = APIEndpoint(
                path=normalized_path,
                method=route["method"],
                summary=route.get("summary"),
                description=route.get("description"),
                operation_id=route.get("operation_id")
                or self._generate_operation_id(normalized_path, route["method"]),
                parameters=parameters,
                request_body=final_request_body,
                responses=responses,
                source_file=self.get_relative_path(file_path),
                source_line=route.get("line"),
            )

            endpoints.append(endpoint)

        return endpoints

    def _extract_carter_routes(self, content: str) -> List[Dict[str, Any]]:
        """Extract app.Map* route definitions from Carter modules."""
        routes: List[Dict[str, Any]] = []
        pattern = re.compile(r'app\.Map(?P<verb>Get|Post|Put|Delete|Patch)\s*\(', re.MULTILINE)

        for match in pattern.finditer(content):
            verb = match.group("verb").upper()
            http_method = getattr(HTTPMethod, verb, None)
            if not http_method:
                continue

            path, _ = self._extract_carter_path(content, match.end())
            if not path:
                continue

            block = self._extract_expression_block(content, match.start())
            metadata = self._extract_carter_metadata(block, content)
            line_number = self._calculate_line_number(content, match.start())
            lambda_params = self._extract_lambda_parameters(block)

            routes.append(
                {
                    "path": path,
                    "method": http_method,
                    "summary": metadata.get("summary"),
                    "description": metadata.get("description"),
                    "operation_id": metadata.get("operation_id"),
                    "line": line_number,
                    "lambda_params": lambda_params,
                    "responses": metadata.get("responses"),
                }
            )

        return routes

    def _extract_carter_path(self, content: str, start_index: int) -> Tuple[str, int]:
        """Extract the first argument (route path) from app.Map* call."""
        idx = start_index
        n = len(content)

        while idx < n and content[idx].isspace():
            idx += 1

        prefix = ""
        while idx < n and content[idx] in ('@', '$'):
            prefix += content[idx]
            idx += 1

        if idx >= n or content[idx] != '"':
            # Not a literal path (could be constant) – skip for now
            return "", idx

        idx += 1
        path_chars = []
        verbatim = "@" in prefix

        while idx < n:
            char = content[idx]

            if char == '"':
                if verbatim:
                    if idx + 1 < n and content[idx + 1] == '"':
                        path_chars.append('"')
                        idx += 2
                        continue
                    else:
                        break
                else:
                    if idx > 0 and content[idx - 1] == "\\":
                        path_chars.append(char)
                        idx += 1
                        continue
                    else:
                        break

            path_chars.append(char)
            idx += 1

        return "".join(path_chars).strip(), idx

    def _extract_expression_block(self, content: str, start_index: int) -> str:
        """Extract the entire route expression up to the terminating semicolon."""
        paren_depth = 0
        brace_depth = 0
        bracket_depth = 0
        in_string = False
        string_char = ""
        i = start_index
        n = len(content)

        while i < n:
            char = content[i]

            if in_string:
                if char == "\\" and string_char == '"' and (i + 1) < n:
                    i += 2
                    continue
                if char == string_char:
                    in_string = False
                    string_char = ""
                i += 1
                continue

            if char in ('"', "'"):
                in_string = True
                string_char = char
            elif char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth = max(0, paren_depth - 1)
            elif char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth = max(0, brace_depth - 1)
            elif char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth = max(0, bracket_depth - 1)
            elif char == ';' and paren_depth == 0 and brace_depth == 0 and bracket_depth == 0:
                return content[start_index:i]

            i += 1

        return content[start_index:]

    def _extract_carter_metadata(self, block: str, file_content: str) -> Dict[str, Any]:
        """Extract WithName/WithSummary/WithDescription metadata."""
        metadata: Dict[str, Any] = {}

        def _extract(pattern: str) -> Optional[str]:
            match = re.search(pattern, block)
            if match:
                return match.group(1).strip()
            return None

        metadata["summary"] = _extract(r'\.WithSummary\s*\(\s*@?"([^"]+)"\s*\)')
        metadata["description"] = _extract(r'\.WithDescription\s*\(\s*@?"([^"]+)"\s*\)')
        metadata["operation_id"] = _extract(r'\.WithName\s*\(\s*@?"([^"]+)"\s*\)')
        metadata["responses"] = self._extract_carter_responses(block, file_content)

        return metadata

    def _extract_carter_responses(self, block: str, file_content: str) -> List[APIResponse]:
        """Extract response metadata from .Produces/.ProducesProblem calls."""
        responses: List[APIResponse] = []
        pattern = re.compile(
            r'\.(Produces|ProducesProblem)(?:<(?P<type>[^>]+)>)?\s*\(\s*(?P<args>[^\)]*)\)',
            re.MULTILINE,
        )

        for match in pattern.finditer(block):
            args = match.group("args") or ""
            tokens = [token.strip() for token in args.split(",") if token.strip()]

            status_code = 200
            body_type: Optional[str] = match.group("type")
            description = "Successful response"

            if match.group(1) == "ProducesProblem":
                description = "Problem response"

            for token in tokens:
                if "StatusCodes" in token or token.isdigit():
                    digits = re.search(r'(\d+)', token)
                    if digits:
                        status_code = int(digits.group(1))
                elif token.startswith("typeof"):
                    inside = re.search(r'typeof\s*\(\s*([^)]+)\s*\)', token)
                    if inside:
                        body_type = inside.group(1).strip()

            schema = None
            if body_type and match.group(1) != "ProducesProblem":
                schema = self._csharp_type_to_schema(body_type, file_content)
            elif match.group(1) == "ProducesProblem":
                schema = {"type": "object"}

            responses.append(
                APIResponse(
                    status_code=status_code,
                    description=description,
                    schema=schema,
                )
            )

        return responses

    def _extract_lambda_parameters(self, block: str) -> List[Dict[str, str]]:
        """Extract lambda parameter definitions from a Carter route."""
        # Find the lambda expression - look for pattern: , async? (...) =>
        # This handles cases like: MapPost("/path", async (Type param) => ...)
        # We need to find the lambda parameters, not the MapPost method call
        lambda_pattern = r',\s*(?:async\s+)?\(([^\)]*)\)\s*=>'
        match = re.search(lambda_pattern, block)
        if not match:
            # Fallback: try to find any (...) => pattern at the end
            lambda_pattern = r'(?:async\s+)?\(([^\)]*)\)\s*=>'
            matches = list(re.finditer(lambda_pattern, block))
            if not matches:
                return []
            # Use the last match
            match = matches[-1]
        
        params_str = match.group(1).strip()
        
        if not params_str:
            return []

        parameters: List[Dict[str, str]] = []
        for raw_param in self._split_parameters(params_str):
            cleaned = raw_param.strip()
            if not cleaned or cleaned == "_":
                continue

            attributes = re.findall(r'\[([^\]]+)\]', cleaned)
            attribute = attributes[-1] if attributes else None
            cleaned = re.sub(r'\[[^\]]+\]\s*', '', cleaned).strip()
            cleaned = re.sub(r'\b(ref|out|in|var)\b', '', cleaned).strip()

            if not cleaned:
                continue

            tokens = cleaned.rsplit(" ", 1)
            if len(tokens) != 2:
                continue

            param_type = tokens[0].strip()
            param_name = tokens[1].strip()
            
            # Clean up any stray parentheses or async keywords from type
            param_type = re.sub(r'^[\s\(]+', '', param_type)  # Remove leading spaces and parentheses
            param_type = re.sub(r'[\s\)]+$', '', param_type)  # Remove trailing spaces and parentheses
            param_type = re.sub(r'^\s*async\s+', '', param_type, flags=re.IGNORECASE)
            param_type = param_type.strip()
            
            # Clean up parameter name
            param_name = re.sub(r'^[\s\(]+', '', param_name)
            param_name = re.sub(r'[\s\)]+$', '', param_name)
            param_name = param_name.strip()

            parameters.append(
                {
                    "type": param_type,
                    "name": param_name,
                    "attribute": attribute,
                }
            )

        return parameters

    def _split_parameters(self, params: str) -> List[str]:
        """Split comma-separated parameter lists safely handling generics."""
        # Strip leading/trailing parentheses from the entire params string
        params = params.strip().lstrip('(').rstrip(')').strip()
        
        parts: List[str] = []
        current: List[str] = []
        depth = 0

        for char in params:
            if char == ',' and depth == 0:
                part = ''.join(current).strip()
                if part:
                    parts.append(part)
                current = []
                continue

            current.append(char)
            if char == '<':
                depth += 1
            elif char == '>':
                depth = max(0, depth - 1)

        if current:
            part = ''.join(current).strip()
            if part:
                parts.append(part)

        return parts

    def _classify_lambda_parameters(
        self,
        lambda_params: List[Dict[str, str]],
        path: str,
        file_content: str,
        existing_parameters: List[APIParameter],
    ) -> Tuple[List[APIParameter], Optional[Dict[str, Any]]]:
        """Classify lambda parameters into query/path/body buckets."""
        additional_params: List[APIParameter] = []
        request_body: Optional[Dict[str, Any]] = None
        path_vars = set(self.extract_path_variables(path))
        existing_map = {param.name: param for param in existing_parameters}

        for param in lambda_params:
            param_type = param.get("type", "").strip()
            param_name = param.get("name", "").strip()
            attribute = (param.get("attribute") or "").split('.')[-1]

            if not param_type or not param_name:
                continue

            base_type = self._normalize_type_name(param_type)
            if self._is_service_parameter(base_type):
                continue

            if param_name in path_vars:
                updated_type = self._csharp_type_to_openapi_type(param_type)
                if param_name in existing_map:
                    existing_map[param_name].type = updated_type
                else:
                    additional_params.append(
                        APIParameter(
                            name=param_name,
                            location=ParameterLocation.PATH,
                            required=True,
                            type=updated_type,
                        )
                    )
                continue

            if attribute.lower() == "fromheader":
                additional_params.append(
                    APIParameter(
                        name=param_name,
                        location=ParameterLocation.HEADER,
                        required=False,
                        type=self._csharp_type_to_openapi_type(param_type),
                    )
                )
                continue

            if attribute.lower() == "fromquery":
                additional_params.append(
                    APIParameter(
                        name=param_name,
                        location=ParameterLocation.QUERY,
                        required=False,
                        type=self._csharp_type_to_openapi_type(param_type),
                    )
                )
                continue

            should_use_body = (
                attribute.lower() == "frombody"
                or not self._is_simple_type(base_type)
            )

            if should_use_body:
                if not request_body:
                    request_body = self._build_request_body(param_type, file_content)
                continue

            additional_params.append(
                APIParameter(
                    name=param_name,
                    location=ParameterLocation.QUERY,
                    required=False,
                    type=self._csharp_type_to_openapi_type(param_type),
                )
            )

        return additional_params, request_body

    def _build_request_body(self, type_name: str, file_content: str) -> Dict[str, Any]:
        """Create a request body schema for the supplied type."""
        schema = self._csharp_type_to_schema(type_name, file_content)
        return {
            "required": True,
            "content": {
                "application/json": {
                    "schema": schema,
                }
            },
        }

    def _is_service_parameter(self, type_name: str) -> bool:
        """Best-effort detection of DI-provided service parameters."""
        base = self._normalize_type_name(type_name)
        if base in self.SERVICE_TYPES:
            return True
        if base.startswith("ILogger"):
            return True
        if base.endswith("Service") or base.endswith("Repository"):
            return True
        if base.startswith("I") and len(base) > 1 and base[1].isupper() and base.endswith("Client"):
            return True
        return False

    def _is_simple_type(self, type_name: str) -> bool:
        """Check if a type is a simple scalar."""
        base = self._normalize_type_name(type_name)
        return base in self.SIMPLE_TYPES

    def _normalize_type_name(self, type_name: str) -> str:
        """Normalize C# type names by stripping namespaces, generics, and nullable markers."""
        if not type_name:
            return ""

        cleaned = type_name.strip()
        cleaned = cleaned.replace("?", "")
        cleaned = cleaned.replace("global::", "")

        if cleaned.endswith("[]"):
            cleaned = cleaned[:-2]

        if "<" in cleaned:
            cleaned = cleaned.split("<", 1)[0]

        if "." in cleaned:
            cleaned = cleaned.split(".")[-1]

        return cleaned.strip()

    def _split_generic_arguments(self, generic_args: str) -> List[str]:
        """Split generic arguments while handling nested generics."""
        parts: List[str] = []
        current: List[str] = []
        depth = 0

        for char in generic_args:
            if char == ',' and depth == 0:
                parts.append(''.join(current).strip())
                current = []
                continue

            current.append(char)
            if char == '<':
                depth += 1
            elif char == '>':
                depth = max(0, depth - 1)

        if current:
            parts.append(''.join(current).strip())

        return [part for part in parts if part]

    def _resolve_complex_type_schema(
        self,
        type_name: str,
        local_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Resolve schema definitions for complex/DTO types."""
        normalized = self._normalize_type_name(type_name)
        if not normalized:
            return {"type": "object"}

        if normalized in self._type_schema_cache:
            return self._type_schema_cache[normalized]

        # Avoid recursive loops by caching placeholder first
        self._type_schema_cache[normalized] = {"type": "object"}

        schema: Optional[Dict[str, Any]] = None

        if local_content:
            schema = self._extract_schema_from_content(local_content, normalized)

        if not schema:
            for content in self._file_content_cache.values():
                schema = self._extract_schema_from_content(content, normalized)
                if schema:
                    break

        if not schema:
            schema = {"type": "object"}

        self._type_schema_cache[normalized] = schema
        return schema

    def _extract_schema_from_content(
        self,
        content: str,
        type_name: str,
    ) -> Optional[Dict[str, Any]]:
        """Extract schema information from record or class definitions."""
        if not content or type_name not in content:
            return None

        positional_pattern = re.compile(
            rf'record\s+{re.escape(type_name)}\s*\((?P<props>[^\)]*)\)',
            re.MULTILINE,
        )
        match = positional_pattern.search(content)
        if match:
            properties = self._parse_record_properties(match.group("props"), content)
            if properties:
                return {
                    "type": "object",
                    "properties": properties,
                    "required": list(properties.keys()),
                }

        # Try to find class/record with body
        class_pattern = re.compile(
            rf'(class|record)\s+{re.escape(type_name)}\s*[^{{]*\{{',
            re.MULTILINE,
        )
        match = class_pattern.search(content)
        if match:
            start_pos = match.end()
            # Extract body with proper brace matching
            brace_depth = 1
            i = start_pos
            n = len(content)
            body_end = start_pos
            
            while i < n and brace_depth > 0:
                if content[i] == '{':
                    brace_depth += 1
                elif content[i] == '}':
                    brace_depth -= 1
                    if brace_depth == 0:
                        body_end = i
                        break
                i += 1
            
            if body_end > start_pos:
                body = content[start_pos:body_end]
                property_pattern = re.compile(
                    r'\bpublic\s+([\w<>\.\[\]]+)\s+(\w+)\s*\{\s*get\s*[^}]*\}',
                    re.MULTILINE,
                )
                properties: Dict[str, Any] = {}
                required: List[str] = []

                for prop_match in property_pattern.finditer(body):
                    prop_type = prop_match.group(1).strip()
                    prop_name = prop_match.group(2).strip()
                    properties[prop_name] = self._csharp_type_to_schema(prop_type, content)
                    required.append(prop_name)

                if properties:
                    schema: Dict[str, Any] = {
                        "type": "object",
                        "properties": properties,
                    }
                    if required:
                        schema["required"] = required
                    return schema

        return None

    def _parse_record_properties(
        self,
        props: str,
        content: str,
    ) -> Dict[str, Any]:
        """Parse positional record constructor properties."""
        properties: Dict[str, Any] = {}

        for prop in self._split_parameters(props):
            cleaned = prop.strip()
            if not cleaned:
                continue

            tokens = cleaned.rsplit(" ", 1)
            if len(tokens) != 2:
                continue

            prop_type = tokens[0].strip()
            prop_name = tokens[1].strip()

            properties[prop_name] = self._csharp_type_to_schema(prop_type, content)

        return properties

    def _unwrap_known_wrappers(self, type_name: str) -> str:
        """Unwrap well-known generic wrappers like Task<T> or ActionResult<T>."""
        if not type_name:
            return type_name

        current = type_name.strip()
        wrappers = {"Task", "ValueTask", "ActionResult", "IActionResult"}

        while True:
            generic_match = re.match(r'([\w\.]+)<(.+)>', current)
            if not generic_match:
                break

            base = self._normalize_type_name(generic_match.group(1))
            if base not in wrappers:
                break

            args = self._split_generic_arguments(generic_match.group(2))
            if not args:
                break

            current = args[0].strip()

        return current

    def _create_path_parameters(self, path: str) -> List[APIParameter]:
        """Create path parameters from a normalized path."""
        parameters: List[APIParameter] = []
        for variable in self.extract_path_variables(path):
            parameters.append(
                APIParameter(
                    name=variable,
                    location=ParameterLocation.PATH,
                    required=True,
                    type="string",
                )
            )
        return parameters

    def _calculate_line_number(self, content: str, char_index: int) -> int:
        """Convert a character index to a 1-based line number."""
        return content.count("\n", 0, char_index) + 1

    def _combine_paths(self, base: str, path: str) -> str:
        """Combine base path and method path."""
        if not base:
            return path
        if not path:
            return base
        
        base = base.rstrip('/')
        path = path.lstrip('/')
        
        return f"{base}/{path}"

    def _extract_parameters(self, signature: str, path: str) -> List[APIParameter]:
        """Extract parameters from method signature."""
        parameters = []
        
        # Extract path parameters
        path_vars = self.extract_path_variables(path)
        for var in path_vars:
            # Try to find [FromRoute] annotation with type
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
        
        # Extract [FromQuery] parameters with types
        pattern = r'\[FromQuery\](?:\([^)]*\))?\s+([\w<>[\],\s]+)\s+(\w+)'
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
        
        # Extract [FromHeader] parameters
        pattern = r'\[FromHeader\](?:\([^)]*\))?\s+([\w<>[\],\s]+)\s+(\w+)'
        for match in re.finditer(pattern, signature):
            param_type = self._csharp_type_to_openapi_type(match.group(1).strip())
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

    def _extract_request_body(
        self,
        signature: str,
        file_content: str,
    ) -> Optional[Dict[str, Any]]:
        """Extract request body from method signature."""
        if not signature:
            return None

        params_match = re.search(r'\((?P<params>[^\)]*)\)', signature)
        if not params_match:
            return None

        params_section = params_match.group("params")

        for param in self._split_parameters(params_section):
            cleaned = param.strip()
            if not cleaned:
                continue

            attributes = re.findall(r'\[([^\]]+)\]', cleaned)
            attribute = attributes[-1] if attributes else ""
            base = re.sub(r'\[[^\]]+\]\s*', '', cleaned).strip()

            tokens = base.rsplit(" ", 1)
            if len(tokens) != 2:
                continue

            param_type = tokens[0].strip()
            attr_lower = attribute.lower()

            if attr_lower == "frombody":
                return self._build_request_body(param_type, file_content)

            if attr_lower in {"fromroute", "fromquery", "fromheader"}:
                continue

            if self._is_service_parameter(param_type):
                continue

            if not self._is_simple_type(param_type):
                return self._build_request_body(param_type, file_content)

        return None

    def _extract_response_schema(
        self,
        signature: str,
        file_content: str,
    ) -> Optional[Dict[str, Any]]:
        """Extract response schema from method return type."""
        if not signature:
            return None

        pattern = r'\s*(?:public|private|protected|internal)?\s+([^\(\)]+?)\s+\w+\s*\('
        match = re.search(pattern, signature)
        if not match:
            return None

        return_type = match.group(1).strip()
        if not return_type or return_type.lower() in {"void"}:
            return None

        unwrapped = self._unwrap_known_wrappers(return_type)
        normalized = self._normalize_type_name(unwrapped)

        if normalized in {"void", "iresult", "actionresult", "iactionresult"}:
            return None

        return self._csharp_type_to_schema(unwrapped, file_content)

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
            "decimal": "number",
            "Decimal": "number",
            "bool": "boolean",
            "Boolean": "boolean",
            "string": "string",
            "String": "string",
            "char": "string",
            "Char": "string",
            "Guid": "string",
            "DateTime": "string",
            "DateOnly": "string",
            "TimeOnly": "string",
        }
        return type_map.get(csharp_type, "string")

    def _csharp_type_to_schema(
        self,
        csharp_type: str,
        local_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convert C# type to OpenAPI schema."""
        if not csharp_type:
            return {"type": "object"}

        csharp_type = csharp_type.strip().replace("global::", "")

        if csharp_type.endswith("[]"):
            inner = csharp_type[:-2].strip()
            return {
                "type": "array",
                "items": self._csharp_type_to_schema(inner, local_content),
            }

        generic_match = re.match(r'([\w\.]+)<(.+)>', csharp_type)
        if generic_match:
            base = self._normalize_type_name(generic_match.group(1))
            args = self._split_generic_arguments(generic_match.group(2))

            if base in {"Task", "ValueTask"} and args:
                return self._csharp_type_to_schema(args[0], local_content)

            if base in {"List", "IList", "ICollection", "IEnumerable", "HashSet"} and args:
                return {
                    "type": "array",
                    "items": self._csharp_type_to_schema(args[0], local_content),
                }

            if base in {"Dictionary", "IDictionary"} and len(args) >= 2:
                return {
                    "type": "object",
                    "additionalProperties": self._csharp_type_to_schema(args[1], local_content),
                }

            if base in {"ActionResult", "IActionResult"} and args:
                return self._csharp_type_to_schema(args[0], local_content)

        if self._is_simple_type(csharp_type):
            return {"type": self._csharp_type_to_openapi_type(csharp_type)}

        return self._resolve_complex_type_schema(csharp_type, local_content)

    def _generate_operation_id(self, path: str, method: HTTPMethod) -> str:
        """Generate operation ID from path and method."""
        path_parts = [p for p in path.split('/') if p and not p.startswith('{')]
        operation_id = method.value.lower() + ''.join(p.capitalize() for p in path_parts)
        return operation_id

