"""
HTTP Request object for dependency injection.
"""

from typing import Dict, Any, Callable, Optional
import json


class Request:
    """
    HTTP Request object.
    
    Provides access to request data for dependencies.
    
    Example:
        async def get_current_user(request: Request):
            token = request.headers.get(b"authorization")
            return await verify_token(token)
        
        @app.get("/me")
        async def get_profile(user = Depends(get_current_user)):
            return user
    """

    def __init__(self, scope: dict, receive: Callable, send: Callable):
        self.scope = scope
        self._receive = receive
        self._send = send
        self._body: Optional[bytes] = None
        self._json: Optional[Dict[str, Any]] = None

    @property
    def method(self) -> str:
        """HTTP method (GET, POST, etc.)."""
        return self.scope["method"]

    @property
    def path(self) -> str:
        """Request path."""
        return self.scope["path"]

    @property
    def headers(self) -> Dict[bytes, bytes]:
        """Request headers as dict."""
        return dict(self.scope.get("headers", []))

    def get_header(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get header value by name (case-insensitive).
        
        Args:
            name: Header name
            default: Default value if header not found
        
        Returns:
            Header value or default
        """
        name_lower = name.lower().encode()
        for key, value in self.headers.items():
            if key.lower() == name_lower:
                return value.decode()
        return default

    @property
    def query_params(self) -> Dict[str, Any]:
        """Query parameters."""
        from urllib.parse import parse_qs
        query_string = self.scope.get("query_string", b"").decode()
        if not query_string:
            return {}
        parsed = parse_qs(query_string)
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

    @property
    def path_params(self) -> Dict[str, str]:
        """Path parameters (if available)."""
        return self.scope.get("path_params", {})

    async def body(self) -> bytes:
        """
        Get request body as bytes.
        
        Returns:
            Request body
        """
        if self._body is None:
            body = b""
            while True:
                message = await self._receive()
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break
            self._body = body
        return self._body

    async def json(self) -> Dict[str, Any]:
        """
        Parse body as JSON.
        
        Returns:
            Parsed JSON data
        
        Raises:
            json.JSONDecodeError: If body is not valid JSON
        """
        if self._json is None:
            body = await self.body()
            self._json = json.loads(body.decode())
        return self._json

    @property
    def client(self) -> Optional[tuple]:
        """Client address (host, port)."""
        return self.scope.get("client")

    @property
    def url(self) -> str:
        """Full URL."""
        scheme = self.scope.get("scheme", "http")
        server = self.scope.get("server", ("localhost", 8000))
        path = self.path
        query = self.scope.get("query_string", b"").decode()

        url = f"{scheme}://{server[0]}:{server[1]}{path}"
        if query:
            url += f"?{query}"
        return url

    def __repr__(self):
        return f"Request(method={self.method}, path={self.path})"
