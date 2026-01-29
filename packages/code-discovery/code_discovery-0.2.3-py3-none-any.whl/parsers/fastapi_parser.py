"""FastAPI parser."""

import ast
import re
from pathlib import Path
from typing import List, Optional, Dict, Any, Set
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


class FastAPIParser(BaseParser):
    """Parser for FastAPI applications."""

    def __init__(self, source_paths: List[Path], repo_path: Path):
        super().__init__(source_paths, repo_path)
        self._file_content_cache: Dict[Path, str] = {}
        self._router_prefixes: Dict[str, str] = {}  # router_name -> prefix (combined)
        self._router_files: Dict[str, Path] = {}  # router_name -> file_path
        self._model_schemas: Dict[str, Dict[str, Any]] = {}  # model_name -> schema
        self._include_router_prefixes: Dict[str, str] = {}  # router_var -> include_router prefix

    def parse(self) -> DiscoveryResult:
        """Parse FastAPI source files for API endpoints."""
        endpoints = []
        py_files = self.find_files("*.py")
        
        # Filter out venv and other non-source directories
        py_files = [f for f in py_files if 'venv' not in str(f) and '__pycache__' not in str(f)]
        
        # First pass: Cache all files and extract models
        for py_file in py_files:
            content = self.read_file(py_file)
            if content:
                try:
                    self._file_content_cache[py_file] = content
                    # Always extract Pydantic models (they might be in separate model files)
                    self._extract_pydantic_models(py_file, content)
                except (SyntaxError, UnicodeDecodeError):
                    continue  # Skip files with syntax errors or encoding issues
        
        # Second pass: Find all router definitions (APIRouter calls)
        for py_file, content in self._file_content_cache.items():
            if self._has_fastapi_imports(content):
                try:
                    self._find_router_definitions(py_file, content)
                except (SyntaxError, AttributeError):
                    continue
        
        # Third pass: Process include_router calls (now we know all router prefixes)
        for py_file, content in self._file_content_cache.items():
            if self._has_fastapi_imports(content):
                try:
                    self._process_include_router_calls(py_file, content)
                except (SyntaxError, AttributeError):
                    continue
        
        # Second pass: Parse endpoints with full context
        for py_file, content in self._file_content_cache.items():
            if self._has_fastapi_imports(content):
                endpoints.extend(self._parse_file(py_file, content))

        return DiscoveryResult(
            framework=FrameworkType.FASTAPI,
            endpoints=endpoints,
            title="FastAPI",
        )

    def get_framework_type(self) -> FrameworkType:
        """Get the framework type."""
        return FrameworkType.FASTAPI

    def _has_fastapi_imports(self, content: str) -> bool:
        """Check if file imports FastAPI."""
        return "from fastapi import" in content or "import fastapi" in content or "fastapi" in content.lower()

    def _find_router_definitions(self, file_path: Path, content: str):
        """Find all APIRouter definitions and their prefixes."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            router_name = target.id
                            if isinstance(node.value, ast.Call):
                                if self._is_apirouter_call(node.value):
                                    prefix = self._extract_router_prefix(node.value)
                                    if prefix:
                                        # Store the router's own prefix
                                        self._router_prefixes[router_name] = prefix
                                        self._router_files[router_name] = file_path
        except (SyntaxError, AttributeError):
            pass
    
    def _process_include_router_calls(self, file_path: Path, content: str):
        """Process include_router calls and combine with router prefixes."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Expr):
                    if isinstance(node.value, ast.Call):
                        if self._is_include_router_call(node.value, content):
                            prefix = self._extract_include_router_prefix(node.value)
                            router_arg = node.value.args[0] if node.value.args else None
                            
                            if router_arg and prefix:
                                # Handle different router argument formats
                                if isinstance(router_arg, ast.Attribute):
                                    # sessions.router
                                    module_name = router_arg.value.id if isinstance(router_arg.value, ast.Name) else None
                                    router_attr = router_arg.attr
                                    
                                    if module_name:
                                        # Find the router name in the module
                                        router_name = self._find_router_in_module(module_name, file_path, content, router_attr)
                                        if not router_name:
                                            # Fallback: use router_attr directly
                                            router_name = router_attr
                                        
                                        # Get router's own prefix and combine
                                        router_own_prefix = self._router_prefixes.get(router_name, "")
                                        if router_own_prefix:
                                            combined = prefix.rstrip('/') + router_own_prefix
                                        else:
                                            combined = prefix
                                        self._router_prefixes[router_name] = combined
                                elif isinstance(router_arg, ast.Name):
                                    # router (direct variable)
                                    router_var = router_arg.id
                                    router_own_prefix = self._router_prefixes.get(router_var, "")
                                    if router_own_prefix:
                                        combined = prefix.rstrip('/') + router_own_prefix
                                    else:
                                        combined = prefix
                                    self._router_prefixes[router_var] = combined
        except (SyntaxError, AttributeError):
            pass

    def _is_apirouter_call(self, call_node: ast.Call) -> bool:
        """Check if call is APIRouter(...)."""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id == 'APIRouter'
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr == 'APIRouter'
        return False

    def _is_include_router_call(self, call_node: ast.Call, content: str) -> bool:
        """Check if call is app.include_router(...) or router.include_router(...)."""
        if isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr == 'include_router'
        return False

    def _extract_router_prefix(self, call_node: ast.Call) -> Optional[str]:
        """Extract prefix from APIRouter(prefix="/path") call."""
        for keyword in call_node.keywords:
            if keyword.arg == 'prefix':
                if isinstance(keyword.value, ast.Constant):
                    return keyword.value.value
                elif isinstance(keyword.value, ast.Str):  # Python < 3.8
                    return keyword.value.s
        return None

    def _extract_include_router_prefix(self, call_node: ast.Call) -> Optional[str]:
        """Extract prefix from app.include_router(router, prefix="/api/v1") call."""
        for keyword in call_node.keywords:
            if keyword.arg == 'prefix':
                if isinstance(keyword.value, ast.Constant):
                    return keyword.value.value
                elif isinstance(keyword.value, ast.Str):  # Python < 3.8
                    return keyword.value.s
                elif isinstance(keyword.value, ast.Attribute):
                    # Handle settings.api_prefix
                    if isinstance(keyword.value.value, ast.Name):
                        if keyword.value.value.id == 'settings' and keyword.value.attr == 'api_prefix':
                            # Try to find the settings value
                            return self._resolve_settings_api_prefix()
        return None
    
    def _resolve_settings_api_prefix(self) -> Optional[str]:
        """Resolve settings.api_prefix to its actual value."""
        # Search all cached files for Settings class
        for file_path, content in self._file_content_cache.items():
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef) and node.name == 'Settings':
                        # Find api_prefix field
                        for item in node.body:
                            if isinstance(item, ast.AnnAssign):
                                if isinstance(item.target, ast.Name) and item.target.id == 'api_prefix':
                                    if isinstance(item.value, ast.Constant):
                                        return item.value.value
                                    elif isinstance(item.value, ast.Str):  # Python < 3.8
                                        return item.value.s
                                    elif hasattr(item.value, 's'):  # Fallback for older Python
                                        return item.value.s
            except (SyntaxError, AttributeError, UnicodeDecodeError):
                continue
        return None

    def _extract_router_variable(self, call_node: ast.Call) -> Optional[str]:
        """Extract router variable from include_router(router, ...) call."""
        if call_node.args:
            arg = call_node.args[0]
            if isinstance(arg, ast.Name):
                return arg.id
            elif isinstance(arg, ast.Attribute):
                # Handle sessions.router - return the module name
                if isinstance(arg.value, ast.Name):
                    # sessions.router -> return "sessions"
                    return arg.value.id
                # router.router -> return "router"
                return arg.attr
        return None

    def _resolve_router_name(self, router_var: str, file_path: Path, content: str) -> Optional[str]:
        """Resolve router variable to actual router name by checking imports."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    # Check if router_var is imported from another module
                    for alias in node.names:
                        if alias.asname == router_var or alias.name == router_var:
                            # Import like: from .endpoints import sessions
                            # Need to check if sessions has a router
                            module_path = self._resolve_module_path(node.module, file_path)
                            if module_path:
                                module_content = self._file_content_cache.get(module_path)
                                if module_content:
                                    # Find router in that module
                                    router_name = self._find_router_name_in_module(module_content)
                                    if router_name:
                                        return router_name
                                    # Also check if the module itself exports a router variable
                                    # For sessions.router, check if sessions module has 'router'
                                    if alias.name == router_var:
                                        # Check for router = APIRouter(...) in that module
                                        router_name = self._find_router_name_in_module(module_content)
                                        if router_name:
                                            return router_name
        except Exception:
            pass
        # If router_var is like "sessions", check if sessions module has "router"
        # This handles the case: from .endpoints import sessions; app.include_router(sessions.router)
        return router_var

    def _resolve_module_path(self, module: str, current_file: Path) -> Optional[Path]:
        """Resolve module path from import statement."""
        if not module:
            return None
        
        # Convert module path to file path
        parts = module.split('.')
        # Remove leading dots (relative imports)
        while parts and parts[0] == '':
            parts.pop(0)
        
        if not parts:
            return None
        
        # Start from current file's directory
        current_dir = current_file.parent
        
        # Navigate up for each leading dot
        if module.startswith('.'):
            dot_count = len(module) - len(module.lstrip('.'))
            for _ in range(dot_count):
                current_dir = current_dir.parent
        
        # Build file path
        file_path = current_dir
        for part in parts:
            file_path = file_path / part
        file_path = file_path.with_suffix('.py')
        
        # Check if file exists in cache
        if file_path in self._file_content_cache:
            return file_path
        
        # Try __init__.py
        init_path = file_path.parent / '__init__.py'
        if init_path in self._file_content_cache:
            return init_path
        
        return None

    def _find_router_name_in_module(self, content: str) -> Optional[str]:
        """Find router variable name in module content."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if isinstance(node.value, ast.Call):
                                if self._is_apirouter_call(node.value):
                                    return target.id
        except Exception:
            pass
        return None
    
    def _find_router_in_module(self, module_name: str, current_file: Path, content: str, router_attr: str = "router") -> Optional[str]:
        """Find router name in an imported module."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if alias.name == module_name or alias.asname == module_name:
                            # Found the import, now find the module file
                            module_path = self._resolve_module_path(node.module, current_file)
                            if module_path:
                                module_content = self._file_content_cache.get(module_path)
                                if module_content:
                                    # Find the router variable with the specified name
                                    router_name = self._find_router_name_in_module(module_content)
                                    if router_name == router_attr:
                                        return router_name
                                    # Also check if there's a variable named router_attr
                                    try:
                                        mod_tree = ast.parse(module_content)
                                        for mod_node in ast.walk(mod_tree):
                                            if isinstance(mod_node, ast.Assign):
                                                for target in mod_node.targets:
                                                    if isinstance(target, ast.Name) and target.id == router_attr:
                                                        if isinstance(mod_node.value, ast.Call):
                                                            if self._is_apirouter_call(mod_node.value):
                                                                return router_attr
                                    except Exception:
                                        pass
        except Exception:
            pass
        return None

    def _extract_pydantic_models(self, file_path: Path, content: str):
        """Extract all Pydantic models from file and cache their schemas."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it's a Pydantic model
                    if self._is_pydantic_model(node):
                        schema = self._extract_model_schema(node, content)
                        if schema:
                            self._model_schemas[node.name] = schema
        except Exception:
            pass

    def _is_pydantic_model(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a Pydantic model."""
        for base in class_node.bases:
            if isinstance(base, ast.Name):
                if base.id == 'BaseModel':
                    return True
            elif isinstance(base, ast.Attribute):
                # Handle pydantic.BaseModel
                if base.attr == 'BaseModel':
                    return True
        return False

    def _extract_model_schema(self, class_node: ast.ClassDef, content: str) -> Optional[Dict[str, Any]]:
        """Extract schema from Pydantic model class."""
        properties = {}
        required = []
        
        # Track field assignments and their types
        field_types = {}
        
        for item in class_node.body:
            if isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    field_name = item.target.id
                    field_type = self._extract_type_annotation(item.annotation)
                    field_types[field_name] = field_type
                    
                    # Check if field has default value
                    is_required = True
                    if item.value is not None:
                        # Check what the value is
                        if isinstance(item.value, ast.Constant):
                            # Has a constant default (like None, "", 0, etc.)
                            if item.value.value is None:
                                # Field: Optional[Type] = None means optional
                                is_required = False
                            else:
                                # Has a non-None default, not required
                                is_required = False
                        elif isinstance(item.value, ast.Call):
                            # Check if it's Field() with default
                            if self._is_field_call(item.value):
                                is_required = self._is_field_required(item.value)
                            else:
                                # Other call (like default_factory), not required
                                is_required = False
                        elif isinstance(item.value, ast.Name):
                            # Field = SomeConstant, not required
                            is_required = False
                    # If item.value is None, field has no default, so it's required
                    
                    if is_required:
                        required.append(field_name)
                    
                    # Extract nested schema for complex types
                    schema_type = self._extract_schema_type(item.annotation, content)
                    properties[field_name] = schema_type
                    
            elif isinstance(item, ast.Assign):
                # Handle Field() definitions: field_name: Type = Field(...)
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        field_name = target.id
                        field_type = field_types.get(field_name, "string")
                        
                        if isinstance(item.value, ast.Call):
                            if self._is_field_call(item.value):
                                # Field has default or default_factory, not required
                                if field_name in required:
                                    required.remove(field_name)
                                
                                # Check if Field specifies a type
                                field_schema = self._extract_field_schema(item.value, field_type, content)
                                if field_schema:
                                    properties[field_name] = field_schema
                                    continue
                        
                        # Default property
                        if field_name not in properties:
                            properties[field_name] = {
                                "type": field_type,
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
    
    def _is_field_call(self, call_node: ast.Call) -> bool:
        """Check if call is Field()."""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id == 'Field'
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr == 'Field'
        return False
    
    def _is_field_required(self, field_call: ast.Call) -> bool:
        """Check if Field() indicates required (no default, no default_factory, not ...)."""
        # Check for Ellipsis (...) which means required
        if field_call.args:
            if isinstance(field_call.args[0], ast.Constant):
                if field_call.args[0].value is ...:
                    return True
            elif isinstance(field_call.args[0], ast.Ellipsis):
                return True
        
        # Check for default or default_factory keywords
        for keyword in field_call.keywords:
            if keyword.arg in ['default', 'default_factory']:
                return False
        
        return True
    
    def _extract_field_schema(self, field_call: ast.Call, default_type: str, content: str) -> Optional[Dict[str, Any]]:
        """Extract schema from Field() call."""
        # For now, return simple type schema
        # Could be enhanced to extract description, examples, etc.
        return {"type": default_type}
    
    def _extract_schema_type(self, annotation: ast.AST, content: str) -> Dict[str, Any]:
        """Extract schema type from annotation, handling nested types."""
        if isinstance(annotation, ast.Name):
            type_name = annotation.id
            # Check if it's a model we know about
            if type_name in self._model_schemas:
                return self._model_schemas[type_name]
            
            # Check if it's a simple type
            type_map = {
                'int': 'integer',
                'float': 'number',
                'bool': 'boolean',
                'str': 'string',
                'dict': 'object',
                'list': 'array',
            }
            if type_name in type_map:
                return {"type": type_map[type_name]}
            
            # Try to find it in cached files
            for cached_content in self._file_content_cache.values():
                schema = self._find_pydantic_model_schema(type_name, cached_content)
                if schema and schema.get("properties"):
                    return schema
            
            return {"type": "object"}
        elif isinstance(annotation, ast.Subscript):
            # Handle List[Type], Optional[Type], Dict[str, Type], etc.
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id == 'List' or annotation.value.id == 'list':
                    # Extract item type
                    if hasattr(annotation, 'slice'):
                        item_type = self._extract_schema_type(annotation.slice, content)
                    elif hasattr(annotation, 'elts'):  # Python < 3.9
                        item_type = self._extract_schema_type(annotation.elts[0], content)
                    else:
                        item_type = {"type": "object"}
                    return {
                        "type": "array",
                        "items": item_type,
                    }
                elif annotation.value.id == 'Optional':
                    # Optional[Type] means type or None
                    if hasattr(annotation, 'slice'):
                        return self._extract_schema_type(annotation.slice, content)
                    elif hasattr(annotation, 'elts'):  # Python < 3.9
                        return self._extract_schema_type(annotation.elts[0], content)
                elif annotation.value.id == 'Dict':
                    return {"type": "object", "additionalProperties": True}
        
        return {"type": "object"}

    def _parse_file(self, file_path: Path, content: str) -> List[APIEndpoint]:
        """Parse a Python file for FastAPI endpoints."""
        endpoints = []
        
        try:
            tree = ast.parse(content)
            
            # Parse function decorators (both sync and async)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    endpoint = self._parse_function(node, content, file_path)
                    if endpoint:
                        endpoints.append(endpoint)
        except SyntaxError as e:
            print(f"Syntax error parsing {file_path}: {e}")
        
        return endpoints

    def _parse_function(
        self,
        func_node: ast.AST,  # Can be FunctionDef or AsyncFunctionDef
        content: str,
        file_path: Path,
    ) -> Optional[APIEndpoint]:
        """Parse a function for FastAPI route decorator."""
        # Check decorators for HTTP methods
        for decorator in func_node.decorator_list:
            endpoint = self._parse_decorator(
                decorator,
                func_node,
                content,
                file_path,
            )
            if endpoint:
                return endpoint
        
        return None

    def _parse_decorator(
        self,
        decorator: ast.AST,
        func_node: ast.AST,  # Can be FunctionDef or AsyncFunctionDef
        content: str,
        file_path: Path,
    ) -> Optional[APIEndpoint]:
        """Parse a decorator for HTTP method and path."""
        # Handle app.get(), router.post(), etc.
        if isinstance(decorator, ast.Call):
            if hasattr(decorator.func, 'attr'):
                method_name = decorator.func.attr.upper()
                if method_name in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    http_method = HTTPMethod[method_name]
                    
                    # Extract path
                    path = self._extract_path_from_decorator(decorator)
                    if not path:
                        path = f"/{func_node.name}"
                    
                    # Get router prefix if applicable
                    router_name = None
                    if hasattr(decorator.func, 'value'):
                        if isinstance(decorator.func.value, ast.Name):
                            router_name = decorator.func.value.id
                        elif isinstance(decorator.func.value, ast.Attribute):
                            # Handle app.router.get() or similar
                            router_name = decorator.func.value.attr
                    
                    # Combine router prefix with path
                    if router_name:
                        # Check for include_router prefix first
                        if router_name in self._include_router_prefixes:
                            include_prefix = self._include_router_prefixes[router_name]
                            router_own_prefix = self._router_prefixes.get(router_name, "")
                            # Combine: include_prefix + router_own_prefix + path
                            full_prefix = include_prefix.rstrip('/') + router_own_prefix
                            path = full_prefix.rstrip('/') + '/' + path.lstrip('/')
                        elif router_name in self._router_prefixes:
                            router_prefix = self._router_prefixes[router_name]
                            path = router_prefix.rstrip('/') + '/' + path.lstrip('/')
                    
                    # Also check for app.include_router prefix in main.py
                    # This is a simplified approach - in practice we'd track this better
                    if 'main.py' in str(file_path) or 'app.py' in str(file_path):
                        # Check if there's a global prefix from settings
                        # For now, we'll rely on the router prefix map
                        pass
                    
                    # Normalize path
                    path = self.normalize_path(path)
                    
                    # Extract parameters
                    parameters = self._extract_parameters_from_function(func_node, path, content, file_path)
                    
                    # Extract request body
                    request_body = self._extract_request_body(func_node, path, content, file_path)
                    
                    # Extract response model
                    response_model = self._extract_response_model(decorator, func_node, content, file_path)
                    
                    # Extract status code from decorator
                    status_code = self._extract_status_code(decorator)
                    
                    # Create endpoint
                    # Get function name (works for both FunctionDef and AsyncFunctionDef)
                    func_name = func_node.name if hasattr(func_node, 'name') else 'unknown'
                    
                    return APIEndpoint(
                        path=path,
                        method=http_method,
                        summary=ast.get_docstring(func_node),
                        operation_id=func_name,
                        parameters=parameters,
                        request_body=request_body,
                        responses=[
                            APIResponse(
                                status_code=status_code,
                                description="Successful response",
                                schema=response_model,
                            )
                        ],
                        source_file=self.get_relative_path(file_path),
                        source_line=func_node.lineno,
                    )
        
        return None

    def _extract_status_code(self, decorator: ast.Call) -> int:
        """Extract status_code from decorator."""
        for keyword in decorator.keywords:
            if keyword.arg == 'status_code':
                if isinstance(keyword.value, ast.Constant):
                    return keyword.value.value
                elif isinstance(keyword.value, ast.Attribute):
                    # Handle status.HTTP_201_CREATED
                    if hasattr(keyword.value, 'attr'):
                        # Try to extract number from constant name
                        attr_name = keyword.value.attr
                        if 'CREATED' in attr_name:
                            return 201
                        elif 'OK' in attr_name:
                            return 200
        return 200

    def _extract_path_from_decorator(self, decorator: ast.Call) -> Optional[str]:
        """Extract path from decorator arguments."""
        # First positional argument
        if decorator.args:
            if isinstance(decorator.args[0], ast.Constant):
                return decorator.args[0].value
            elif isinstance(decorator.args[0], ast.Str):  # Python < 3.8
                return decorator.args[0].s
        
        # Keyword argument 'path'
        for keyword in decorator.keywords:
            if keyword.arg == 'path':
                if isinstance(keyword.value, ast.Constant):
                    return keyword.value.value
                elif isinstance(keyword.value, ast.Str):  # Python < 3.8
                    return keyword.value.s
        
        return None

    def _extract_response_model(
        self, decorator: ast.Call, func_node: ast.AST, content: str, file_path: Path
    ) -> Optional[Dict[str, Any]]:
        """Extract response_model from decorator and return type."""
        # Check decorator for response_model
        response_model_name = None
        for keyword in decorator.keywords:
            if keyword.arg == 'response_model':
                response_model_name = self._extract_type_name_from_ast(keyword.value)
        
        # Check function return type annotation (works for both FunctionDef and AsyncFunctionDef)
        if not response_model_name and hasattr(func_node, 'returns') and func_node.returns:
            response_model_name = self._extract_type_name_from_ast(func_node.returns)
        
        if response_model_name:
            # Try to find the model definition in cache
            if response_model_name in self._model_schemas:
                return self._model_schemas[response_model_name]
            
            # Search all cached files
            for cached_content in self._file_content_cache.values():
                schema = self._find_pydantic_model_schema(response_model_name, cached_content)
                if schema and schema.get("properties"):
                    return schema
        
        return None

    def _extract_type_name_from_ast(self, node: ast.AST) -> Optional[str]:
        """Extract type name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            # Handle List[Model], Optional[Model], etc.
            if isinstance(node.value, ast.Name):
                if node.value.id in ['List', 'Optional', 'Union']:
                    if hasattr(node, 'slice'):
                        slice_node = node.slice
                        if isinstance(slice_node, ast.Name):
                            return slice_node.id
                        elif isinstance(slice_node, ast.Index):  # Python < 3.9
                            if isinstance(slice_node.value, ast.Name):
                                return slice_node.value.id
        elif isinstance(node, ast.Attribute):
            # Handle models.Model
            return node.attr
        return None

    def _extract_parameters_from_function(
        self,
        func_node: ast.AST,  # Can be FunctionDef or AsyncFunctionDef
        path: str,
        content: str,
        file_path: Path,
    ) -> List[APIParameter]:
        """Extract parameters from function signature."""
        parameters = []
        
        # Extract path parameters
        path_vars = self.extract_path_variables(path)
        
        # Analyze function arguments (works for both FunctionDef and AsyncFunctionDef)
        if not hasattr(func_node, 'args'):
            return parameters
        for arg in func_node.args.args:
            arg_name = arg.arg
            
            # Skip 'self' and 'cls'
            if arg_name in ['self', 'cls']:
                continue
            
            # Check for FastAPI parameter annotations (Path, Query, Header, etc.)
            location, required, param_type = self._extract_fastapi_parameter_info(
                arg, arg_name, path_vars, func_node, content
            )
            
            if location != ParameterLocation.BODY:  # Body params are handled separately
                parameters.append(
                    APIParameter(
                        name=arg_name,
                        location=location,
                        required=required,
                        type=param_type,
                    )
                )
        
        return parameters

    def _extract_fastapi_parameter_info(
        self,
        arg: ast.arg,
        arg_name: str,
        path_vars: List[str],
        func_node: ast.AST,  # Can be FunctionDef or AsyncFunctionDef
        content: str,
    ) -> tuple:
        """Extract FastAPI parameter information."""
        # Default values
        location = ParameterLocation.QUERY
        required = True
        param_type = "string"
        
        # Check if it's a path parameter
        if arg_name in path_vars:
            location = ParameterLocation.PATH
            required = True
        else:
            # Check for Query() default values which indicate query params
            required = self._is_parameter_required(arg, func_node)
        
        # Extract type annotation
        if arg.annotation:
            param_type = self._extract_type_annotation(arg.annotation)
        
        return location, required, param_type

    def _is_parameter_required(self, arg: ast.arg, func_node: ast.AST) -> bool:
        """Check if parameter is required (no default value)."""
        if not func_node.args.defaults:
            return True
        
        # Calculate index of this argument
        arg_index = func_node.args.args.index(arg)
        # Skip 'self' or 'cls' if present
        if func_node.args.args and func_node.args.args[0].arg in ['self', 'cls']:
            arg_index -= 1
        
        # Check if there's a default value for this argument
        defaults_start = len(func_node.args.args) - len(func_node.args.defaults)
        if arg_index < defaults_start:
            return True
        
        return False

    def _extract_request_body(
        self, func_node: ast.AST, path: str, content: str, file_path: Path
    ) -> Optional[Dict[str, Any]]:
        """Extract request body from FastAPI function."""
        # Only for POST, PUT, PATCH methods
        path_vars = self.extract_path_variables(path)
        
        if not hasattr(func_node, 'args'):
            return None
        for arg in func_node.args.args:
            if arg.arg in ['self', 'cls']:
                continue
            
            # Check if parameter has a type annotation that looks like a Pydantic model
            if arg.annotation:
                type_name = self._extract_type_name_from_ast(arg.annotation)
                if type_name:
                    # Check if it's not a path variable
                    if arg.arg not in path_vars:
                        # Try to find Pydantic model schema in cache
                        if type_name in self._model_schemas:
                            schema = self._model_schemas[type_name]
                            return {
                                "required": True,
                                "content": {
                                    "application/json": {
                                        "schema": schema,
                                    }
                                },
                            }
                        
                        # Search all cached files
                        for cached_content in self._file_content_cache.values():
                            schema = self._find_pydantic_model_schema(type_name, cached_content)
                            if schema and schema.get("properties"):
                                return {
                                    "required": True,
                                    "content": {
                                        "application/json": {
                                            "schema": schema,
                                        }
                                    },
                                }
        
        return None

    def _find_pydantic_model_schema(self, model_name: str, content: str) -> Optional[Dict[str, Any]]:
        """Find Pydantic model definition and extract schema."""
        try:
            tree = ast.parse(content)
            
            # Look for class definition with BaseModel
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == model_name:
                    if self._is_pydantic_model(node):
                        return self._extract_model_schema(node, content)
        except Exception:
            pass
        
        return None

    def _extract_type_annotation(self, annotation: ast.AST) -> str:
        """Extract type from annotation."""
        if isinstance(annotation, ast.Name):
            type_map = {
                'int': 'integer',
                'float': 'number',
                'bool': 'boolean',
                'str': 'string',
                'dict': 'object',
                'list': 'array',
            }
            return type_map.get(annotation.id, 'string')
        elif isinstance(annotation, ast.Subscript):
            # Handle List[int], Dict[str, int], etc.
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id == 'List':
                    return 'array'
                elif annotation.value.id == 'Dict':
                    return 'object'
        return 'string'
