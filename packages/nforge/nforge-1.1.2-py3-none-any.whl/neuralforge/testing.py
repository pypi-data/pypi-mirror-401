"""
Test client for NeuralForge applications.

Provides easy testing of NeuralForge endpoints.
"""

from typing import Dict, Optional, Any

import httpx


class TestClient:
    """
    Test client for NeuralForge applications.
    
    Provides async HTTP client for testing endpoints without running a server.
    
    Usage:
        from neuralforge import NeuralForge
        from neuralforge.testing import TestClient
        
        app = NeuralForge()
        
        @app.endpoint("/predict", methods=["POST"])
        async def predict(text: str):
            return {"sentiment": "positive"}
        
        # Test the endpoint
        async with TestClient(app) as client:
            response = await client.post("/predict", json={"text": "Great!"})
            assert response.status_code == 200
            assert response.json()["sentiment"] == "positive"
    
    Features:
    - Async context manager
    - GET, POST, PUT, DELETE methods
    - JSON request/response handling
    - Header management
    - Query parameter support
    """
    def __init__(self, app, base_url: str = "http://testserver"):
        """
        Initialize test client.
        
        Args:
            app: NeuralForge application instance
            base_url: Base URL for requests (default: http://testserver)
        """
        self.app = app
        self.base_url = base_url
        # Use ASGITransport to test ASGI app directly without real HTTP requests
        transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=transport, base_url=base_url)

    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> httpx.Response:
        """
        Make GET request.
        
        Args:
            url: URL path
            params: Query parameters
            headers: Request headers
            **kwargs: Additional arguments for httpx
        
        Returns:
            Response object
        
        Example:
            response = await client.get("/models", params={"status": "production"})
        """
        return await self.client.get(url, params=params, headers=headers, **kwargs)

    async def post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> httpx.Response:
        """
        Make POST request.
        
        Args:
            url: URL path
            json: JSON request body
            data: Form data
            headers: Request headers
            **kwargs: Additional arguments for httpx
        
        Returns:
            Response object
        
        Example:
            response = await client.post(
                "/predict",
                json={"text": "This is great!"}
            )
        """
        return await self.client.post(
            url,
            json=json,
            data=data,
            headers=headers,
            **kwargs
        )

    async def put(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> httpx.Response:
        """
        Make PUT request.
        
        Args:
            url: URL path
            json: JSON request body
            data: Form data
            headers: Request headers
            **kwargs: Additional arguments for httpx
        
        Returns:
            Response object
        
        Example:
            response = await client.put(
                "/models/sentiment_v1",
                json={"status": "production"}
            )
        """
        return await self.client.put(
            url,
            json=json,
            data=data,
            headers=headers,
            **kwargs
        )

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> httpx.Response:
        """
        Make DELETE request.
        
        Args:
            url: URL path
            headers: Request headers
            **kwargs: Additional arguments for httpx
        
        Returns:
            Response object
        
        Example:
            response = await client.delete("/models/old_model")
        """
        return await self.client.delete(url, headers=headers, **kwargs)

    async def patch(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> httpx.Response:
        """
        Make PATCH request.
        
        Args:
            url: URL path
            json: JSON request body
            headers: Request headers
            **kwargs: Additional arguments for httpx
        
        Returns:
            Response object
        
        Example:
            response = await client.patch(
                "/models/sentiment_v1",
                json={"metrics": {"accuracy": 0.96}}
            )
        """
        return await self.client.patch(url, json=json, headers=headers, **kwargs)

    async def __aenter__(self):
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager and cleanup."""
        await self.client.aclose()

    async def close(self):
        """Close the client connection."""
        await self.client.aclose()


__all__ = ["TestClient"]
