"""
Router - Request routing and handling.
"""

from typing import Callable, List, Dict, Any, Optional, get_type_hints
import inspect
import logging
import re
import json
from urllib.parse import parse_qs
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class Route:
    """Represents a single route in the application."""

    def __init__(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str],
        name: Optional[str] = None,
        tags: List[str] = None,
        **kwargs
    ):
        self.path = path
        self.endpoint = endpoint
        self.methods = [m.upper() for m in methods]
        self.name = name or endpoint.__name__
        self.tags = tags or []
        self.metadata = kwargs

        # Extract type hints for validation
        self.signature = inspect.signature(endpoint)
        self.return_type = self.signature.return_annotation

    def __repr__(self) -> str:
        methods_str = ",".join(self.methods)
        return f"<Route(path='{self.path}', methods=[{methods_str}])>"


class Router:
    """
    Router for handling HTTP requests and WebSocket connections.
    
    Maps URLs to endpoint functions.
    """

    def __init__(self):
        self.routes: List[Route] = []
        self.websocket_routes: List[Route] = []
        self.mounts: Dict[str, Any] = {}

        logger.info("Initialized Router")

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str],
        **kwargs
    ):
        """Add an HTTP route."""
        route = Route(
            path=path,
            endpoint=endpoint,
            methods=methods,
            **kwargs
        )
        self.routes.append(route)

        logger.debug(
            f"Added route: {','.join(methods)} {path} -> {endpoint.__name__}"
        )

    def add_websocket_route(self, path: str, endpoint: Callable, **kwargs):
        """Add a WebSocket route."""
        route = Route(
            path=path,
            endpoint=endpoint,
            methods=["WEBSOCKET"],
            **kwargs
        )
        self.websocket_routes.append(route)

        logger.debug(f"Added WebSocket route: {path} -> {endpoint.__name__}")

    def mount(self, path: str, app: Any, name: str = None):
        """Mount a sub-application."""
        self.mounts[path] = {"app": app, "name": name}
        logger.debug(f"Mounted sub-app at: {path}")

    def include_router(self, router: "Router", prefix: str = "", tags: List[str] = None):
        """Include routes from another router."""
        for route in router.routes:
            route.path = prefix + route.path
            if tags:
                route.tags.extend(tags)
            self.routes.append(route)

        for route in router.websocket_routes:
            route.path = prefix + route.path
            if tags:
                route.tags.extend(tags)
            self.websocket_routes.append(route)

        logger.debug(f"Included router with prefix: {prefix}")

    async def handle(self, scope: dict, receive: Callable, send: Callable):
        """
        Handle incoming request.
        
        This is called by the ASGI application.
        """
        from neuralforge.http import Request
        from neuralforge.dependencies import DependencyResolver

        # Handle WebSocket connections separately
        if scope.get("type") == "websocket":
            await self._handle_websocket(scope, receive, send)
            return

        path = scope["path"]
        method = scope["method"]

        # Find matching route
        route = self._match_route(path, method)

        if route is None:
            await self._send_404(send)
            return

        # Create request object for dependencies
        request = Request(scope, receive, send)

        # Create dependency resolver for this request
        resolver = DependencyResolver()

        # Execute endpoint
        try:
            # Extract path parameters
            path_params = self._extract_path_params(route.path, path)

            # Store path params in scope for dependencies
            scope["path_params"] = path_params

            # Parse query parameters
            query_params = self._parse_query_params(scope)

            # Parse headers
            headers = self._parse_headers(scope.get("headers", []))

            # Parse request body if needed
            body_data = {}
            if method in ["POST", "PUT", "PATCH"]:
                content_type = self._get_content_type(scope)
                body = await self._receive_body(receive)

                if body:
                    try:
                        # Handle form-urlencoded data
                        if "application/x-www-form-urlencoded" in content_type:
                            body_data = self._parse_form_data(body)
                        else:
                            body_data = await self._parse_request_body(body, content_type)
                    except ValueError as e:
                        await self._send_400(send, str(e))
                        return

            # Add headers to body_data for parameter resolution
            # Convert header names: x-api-key -> x_api_key
            for header_name, header_value in headers.items():
                param_name = header_name.replace('-', '_')
                if param_name not in body_data:
                    body_data[param_name] = header_value

            # Prepare endpoint arguments (including dependencies)
            endpoint_kwargs = await self._prepare_endpoint_args(
                route, path_params, query_params, body_data, request, resolver
            )

            # Call endpoint
            if inspect.iscoroutinefunction(route.endpoint):
                result = await route.endpoint(**endpoint_kwargs)
            else:
                result = route.endpoint(**endpoint_kwargs)

            # Send response
            await self._send_response(send, result)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            await self._send_422(send, e.errors())
        except Exception as e:
            # Check if it's an HTTP exception
            from .exceptions import (
                HTTPException, UnauthorizedException, ForbiddenException,
                NotFoundException, BadRequestException
            )

            if isinstance(e, UnauthorizedException):
                await self._send_401(send, str(e))
            elif isinstance(e, ForbiddenException):
                await self._send_403(send, str(e))
            elif isinstance(e, NotFoundException):
                await self._send_404(send)
            elif isinstance(e, BadRequestException):
                await self._send_400(send, str(e))
            elif isinstance(e, HTTPException):
                await self._send_error(send, e.status_code, str(e))
            else:
                logger.error(f"Error handling request: {e}", exc_info=True)
                await self._send_500(send, str(e))
        finally:
            # Clear request-scoped dependencies
            resolver.clear_request_cache()

    def _match_route(self, path: str, method: str) -> Optional[Route]:
        """Find route matching path and method."""
        for route in self.routes:
            if self._path_matches(route.path, path) and method in route.methods:
                return route
        return None

    async def _handle_websocket(self, scope: dict, receive: Callable, send: Callable):
        """Handle WebSocket connection."""
        path = scope["path"]
        
        # Find matching websocket route
        ws_route = None
        for route in self.websocket_routes:
            if self._path_matches(route.path, path):
                ws_route = route
                break
        
        if ws_route is None:
            # No matching websocket route - close connection
            await send({"type": "websocket.close", "code": 4004})
            return
        
        # Create a simple WebSocket wrapper that uvicorn expects
        class WebSocket:
            def __init__(self, scope, receive, send):
                self._scope = scope
                self._receive = receive
                self._send = send
                self._accepted = False
            
            async def accept(self):
                if not self._accepted:
                    await self._send({"type": "websocket.accept"})
                    self._accepted = True
            
            async def send_text(self, data: str):
                await self._send({"type": "websocket.send", "text": data})
            
            async def send_bytes(self, data: bytes):
                await self._send({"type": "websocket.send", "bytes": data})
            
            async def receive_text(self) -> str:
                message = await self._receive()
                if message["type"] == "websocket.disconnect":
                    raise Exception("WebSocket disconnected")
                return message.get("text", "")
            
            async def receive(self) -> dict:
                return await self._receive()
            
            async def close(self, code: int = 1000, reason: str = ""):
                await self._send({"type": "websocket.close", "code": code})
        
        # Create websocket and call handler
        websocket = WebSocket(scope, receive, send)
        try:
            await ws_route.endpoint(websocket)
        except Exception as e:
            logger.error(f"WebSocket handler error: {e}")
            try:
                await websocket.close(code=1011)
            except:
                pass

    def _path_matches(self, pattern: str, path: str) -> bool:
        """Check if path matches pattern with parameter support."""
        regex_pattern = self._pattern_to_regex(pattern)
        match = re.match(regex_pattern, path)
        return match is not None

    def _pattern_to_regex(self, pattern: str) -> str:
        """Convert path pattern to regex (e.g., /users/{id} -> /users/(?P<id>[^/]+))."""
        # Escape special regex characters except {}
        pattern = re.sub(r'([.^$+?\[\]\\|()])', r'\\\1', pattern)
        # Convert {param} to named groups
        pattern = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', pattern)
        return f"^{pattern}$"

    def _extract_path_params(self, pattern: str, path: str) -> Dict[str, str]:
        """Extract path parameters from URL."""
        regex_pattern = self._pattern_to_regex(pattern)
        match = re.match(regex_pattern, path)
        return match.groupdict() if match else {}

    def _parse_query_params(self, scope: dict) -> Dict[str, Any]:
        """Parse query parameters from scope."""
        query_string = scope.get("query_string", b"").decode()
        if not query_string:
            return {}

        # parse_qs returns lists, get first value for simplicity
        parsed = parse_qs(query_string)
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

    def _parse_headers(self, headers: list) -> Dict[str, str]:
        """Parse headers from ASGI scope.
        
        Args:
            headers: List of (name, value) tuples from ASGI scope
        
        Returns:
            Dictionary of header names (lowercase) to values
        """
        header_dict = {}
        for name, value in headers:
            if isinstance(name, bytes):
                name = name.decode('latin1')
            if isinstance(value, bytes):
                value = value.decode('latin1')
            header_dict[name.lower()] = value
        return header_dict

    def _parse_form_data(self, body: bytes) -> Dict[str, Any]:
        """Parse application/x-www-form-urlencoded data.
        
        Args:
            body: Raw body bytes
        
        Returns:
            Dictionary of form field names to values
        """
        if not body:
            return {}

        try:
            form_string = body.decode('utf-8')
            parsed = parse_qs(form_string)
            # Convert lists to single values
            return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        except Exception:
            return {}

    def _convert_param_type(self, value: str, param_type: type) -> Any:
        """Convert string parameter to expected type."""
        if param_type == int:
            return int(value)
        elif param_type == float:
            return float(value)
        elif param_type == bool:
            return value.lower() in ('true', '1', 'yes')
        return value

    async def _receive_body(self, receive: Callable) -> bytes:
        """Receive request body."""
        body = b""
        while True:
            message = await receive()
            body += message.get("body", b"")
            if not message.get("more_body"):
                break
        return body

    def _get_content_type(self, scope: dict) -> str:
        """Extract content-type from headers."""
        headers = dict(scope.get("headers", []))
        content_type = headers.get(b"content-type", b"application/json").decode()
        return content_type

    async def _parse_request_body(self, body: bytes, content_type: str) -> Dict[str, Any]:
        """Parse request body based on content type."""
        if not body:
            return {}

        if "application/json" in content_type:
            try:
                return json.loads(body.decode())
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON: {e}")

        elif "application/x-www-form-urlencoded" in content_type:
            parsed = parse_qs(body.decode())
            # Flatten single values
            return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

        elif "multipart/form-data" in content_type:
            return await self._parse_multipart(body, content_type)

        else:
            # Return raw body as string for unknown types
            return {"body": body.decode()}

    async def _parse_multipart(self, body: bytes, content_type: str) -> Dict[str, Any]:
        """Parse multipart/form-data for file uploads."""
        from .upload import UploadFile

        # Extract boundary from content-type
        if "boundary=" not in content_type:
            raise ValueError("Missing boundary in multipart/form-data")

        boundary = content_type.split("boundary=")[1].strip()
        boundary_bytes = f"--{boundary}".encode()

        # Split by boundary
        parts = body.split(boundary_bytes)

        result = {}
        for part in parts:
            if not part or part == b"--\r\n" or part == b"--":
                continue

            # Remove leading/trailing whitespace
            part = part.strip()
            if not part:
                continue

            # Split headers and content
            if b"\r\n\r\n" in part:
                headers_section, content = part.split(b"\r\n\r\n", 1)
            else:
                continue

            # Parse headers
            headers = headers_section.decode()

            # Extract field name
            name_match = re.search(r'name="([^"]+)"', headers)
            if not name_match:
                continue

            field_name = name_match.group(1)

            # Check if it's a file
            filename_match = re.search(r'filename="([^"]+)"', headers)
            if filename_match:
                filename = filename_match.group(1)

                # Extract content type
                content_type_match = re.search(r'Content-Type: ([^\r\n]+)', headers)
                file_content_type = content_type_match.group(1) if content_type_match else "application/octet-stream"

                # Remove trailing \r\n
                content = content.rstrip(b"\r\n")

                result[field_name] = UploadFile(
                    filename=filename,
                    content=content,
                    content_type=file_content_type
                )
            else:
                # Regular form field
                result[field_name] = content.rstrip(b"\r\n").decode()

        return result

    async def _send_response(self, send: Callable, result: Any):
        """Send HTTP response."""
        from datetime import datetime, date
        from neuralforge.streaming import SSEResponse, TokenStreamResponse, StreamingResponse

        # Handle ASGI-callable response objects (e.g., HTMLResponse)
        # These have a __call__ method that takes (scope, receive, send)
        if hasattr(result, '__call__') and not isinstance(result, (dict, list, str, bytes, type)):
            import inspect
            sig = inspect.signature(result.__call__)
            params = list(sig.parameters.keys())
            # Check if it looks like an ASGI callable (scope, receive, send pattern)
            if len(params) >= 3 or 'send' in params:
                # It's an ASGI response, invoke it directly
                await result(None, None, send)
                return

        # Handle specialized response objects
        status_code = 200
        headers = {b"content-type": b"application/json"}

        # Handle streaming responses
        if isinstance(result, (SSEResponse, TokenStreamResponse, StreamingResponse)) or hasattr(result, '__aiter__'):
            # Start response
            await send({
                "type": "http.response.start",
                "status": status_code,
                "headers": [[k, v] for k, v in headers.items()],
            })

            # Iterate and stream
            async for chunk in result:
                if isinstance(chunk, str):
                    chunk = chunk.encode('utf-8')
                
                await send({
                    "type": "http.response.body",
                    "body": chunk,
                    "more_body": True,
                })
            
            # End stream
            await send({
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            })
            return

        # Custom JSON encoder for datetime
        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                return super().default(obj)

        # Serialize result
        if isinstance(result, BaseModel):
            content = result.model_dump_json().encode()
        elif isinstance(result, (dict, list)):
            content = json.dumps(result, cls=DateTimeEncoder).encode()
        elif isinstance(result, str):
            content = result.encode()
        else:
            content = str(result).encode()

        # Send response
        headers[b"content-length"] = str(len(content)).encode()
        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": [[k, v] for k, v in headers.items()],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _send_404(self, send: Callable):
        """Send 404 Not Found response."""
        content = b'{"error": "Not Found"}'

        await send({
            "type": "http.response.start",
            "status": 404,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(content)).encode()],
            ],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _send_401(self, send: Callable, message: str = "Unauthorized"):
        """Send 401 Unauthorized response."""
        import json
        content = json.dumps({"error": "Unauthorized", "detail": message}).encode()

        await send({
            "type": "http.response.start",
            "status": 401,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(content)).encode()],
            ],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _send_error(self, send: Callable, status_code: int, message: str):
        """Send generic HTTP error response."""
        import json
        content = json.dumps({"error": "Error", "detail": message}).encode()

        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(content)).encode()],
            ],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _send_403(self, send: Callable, message: str = "Forbidden"):
        """Send 403 Forbidden response."""
        import json
        content = json.dumps({"error": "Forbidden", "detail": message}).encode()

        await send({
            "type": "http.response.start",
            "status": 403,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(content)).encode()],
            ],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _send_500(self, send: Callable, error: str):
        """Send 500 Internal Server Error response."""
        import json

        content = json.dumps({"error": "Internal Server Error", "detail": error}).encode()

        await send({
            "type": "http.response.start",
            "status": 500,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(content)).encode()],
            ],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _send_400(self, send: Callable, message: str):
        """Send 400 Bad Request response."""
        import json

        content = json.dumps({"error": "Bad Request", "detail": message}).encode()

        await send({
            "type": "http.response.start",
            "status": 400,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(content)).encode()],
            ],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _send_422(self, send: Callable, errors: list):
        """Send 422 Unprocessable Entity response."""
        import json

        content = json.dumps({"error": "Validation Error", "details": errors}).encode()

        await send({
            "type": "http.response.start",
            "status": 422,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(content)).encode()],
            ],
        })

        await send({
            "type": "http.response.body",
            "body": content,
        })

    async def _prepare_endpoint_args(
        self,
        route: Route,
        path_params: Dict[str, str],
        query_params: Dict[str, Any],
        body_data: Dict[str, Any],
        request: "Request",
        resolver: "DependencyResolver"
    ) -> Dict[str, Any]:
        """Prepare arguments for endpoint function including dependencies."""
        from neuralforge.dependencies import Depends

        sig = route.signature
        kwargs = {}

        # Get type hints
        try:
            type_hints = get_type_hints(route.endpoint)
        except Exception:  # Catch only Exception, not SystemExit/KeyboardInterrupt
            type_hints = {}

        for param_name, param in sig.parameters.items():
            # Skip self/cls
            if param_name in ('self', 'cls'):
                continue

            # Get parameter type
            param_type = type_hints.get(param_name, param.annotation)

            # Check if it's a dependency
            if isinstance(param.default, Depends):
                # Resolve dependency - pass query params AND body_data (includes headers)
                kwargs[param_name] = await resolver.resolve(
                    param.default.dependency,
                    param.default.scope,
                    request=request,
                    **{**query_params, **body_data}  # Merge query params and body_data (headers)
                )
                continue

            # Check if it's an UploadFile
            if param_type != inspect.Parameter.empty:
                try:
                    from .upload import UploadFile
                    if param_type == UploadFile or (isinstance(param_type, type) and issubclass(param_type, UploadFile)):
                        # Look for file in body_data
                        if param_name in body_data and isinstance(body_data[param_name], UploadFile):
                            kwargs[param_name] = body_data[param_name]
                            continue
                except (TypeError, ImportError):
                    pass

            # Check if it's a Pydantic model (request body)
            if param_type != inspect.Parameter.empty:
                try:
                    if isinstance(param_type, type) and issubclass(param_type, BaseModel):
                        # Validate and parse request body
                        kwargs[param_name] = param_type(**body_data)
                        continue
                except (TypeError, ValidationError):
                    pass

            # Check path parameters
            if param_name in path_params:
                value = path_params[param_name]
                # Convert type if hint available
                if param_type != inspect.Parameter.empty and param_type in (int, float, bool):
                    value = self._convert_param_type(value, param_type)
                kwargs[param_name] = value
                continue

            # Check query parameters
            if param_name in query_params:
                value = query_params[param_name]
                # Convert type if hint available
                if param_type != inspect.Parameter.empty and param_type in (int, float, bool):
                    if isinstance(value, str):
                        value = self._convert_param_type(value, param_type)
                kwargs[param_name] = value
                continue

            # Check body data (form fields or JSON)
            if param_name in body_data:
                kwargs[param_name] = body_data[param_name]
                continue

            # Use default value if available
            if param.default != inspect.Parameter.empty:
                kwargs[param_name] = param.default

        return kwargs

    def get_openapi_schema(
        self,
        title: str,
        version: str,
        description: str
    ) -> Dict[str, Any]:
        """Generate OpenAPI schema for all routes."""
        paths = {}

        for route in self.routes:
            if route.path not in paths:
                paths[route.path] = {}

            for method in route.methods:
                paths[route.path][method.lower()] = {
                    "summary": route.name,
                    "operationId": f"{method.lower()}_{route.name}",
                    "tags": route.tags,
                    "responses": {
                        "200": {
                            "description": "Successful Response"
                        }
                    }
                }

        return {
            "openapi": "3.0.0",
            "info": {
                "title": title,
                "version": version,
                "description": description
            },
            "paths": paths
        }
