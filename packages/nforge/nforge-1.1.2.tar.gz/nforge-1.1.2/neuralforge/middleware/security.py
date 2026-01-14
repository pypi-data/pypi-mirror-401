"""
Security Headers Middleware - OWASP recommended security headers.
"""

from typing import Callable, Dict
import logging

from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseMiddleware):
    """
    Security headers middleware implementing OWASP best practices.
    
    Adds security headers to all responses:
    - Strict-Transport-Security (HSTS)
    - Content-Security-Policy (CSP)
    - X-Frame-Options
    - X-Content-Type-Options
    - X-XSS-Protection
    - Referrer-Policy
    - Permissions-Policy
    """

    def __init__(
        self,
        hsts_enabled: bool = True,
        hsts_max_age: int = 31536000,  # 1 year
        hsts_include_subdomains: bool = True,
        csp_enabled: bool = True,
        csp_policy: str = "default-src 'self'",
        x_frame_options: str = "DENY",
        x_content_type_options: bool = True,
        referrer_policy: str = "strict-origin-when-cross-origin"
    ):
        """
        Initialize security headers middleware.
        
        Args:
            hsts_enabled: Enable HTTP Strict Transport Security
            hsts_max_age: HSTS max age in seconds
            hsts_include_subdomains: Include subdomains in HSTS
            csp_enabled: Enable Content Security Policy
            csp_policy: CSP policy string
            x_frame_options: X-Frame-Options value (DENY, SAMEORIGIN)
            x_content_type_options: Enable X-Content-Type-Options: nosniff
            referrer_policy: Referrer-Policy value
        """
        self.hsts_enabled = hsts_enabled
        self.hsts_max_age = hsts_max_age
        self.hsts_include_subdomains = hsts_include_subdomains
        self.csp_enabled = csp_enabled
        self.csp_policy = csp_policy
        self.x_frame_options = x_frame_options
        self.x_content_type_options = x_content_type_options
        self.referrer_policy = referrer_policy

        logger.info("Security headers middleware initialized")

    def _get_security_headers(self) -> Dict[bytes, bytes]:
        """Get security headers to add to response."""
        headers = {}

        # HSTS
        if self.hsts_enabled:
            hsts_value = f"max-age={self.hsts_max_age}"
            if self.hsts_include_subdomains:
                hsts_value += "; includeSubDomains"
            headers[b"Strict-Transport-Security"] = hsts_value.encode()

        # CSP
        if self.csp_enabled:
            headers[b"Content-Security-Policy"] = self.csp_policy.encode()

        # X-Frame-Options
        if self.x_frame_options:
            headers[b"X-Frame-Options"] = self.x_frame_options.encode()

        # X-Content-Type-Options
        if self.x_content_type_options:
            headers[b"X-Content-Type-Options"] = b"nosniff"

        # X-XSS-Protection (legacy, but still useful)
        headers[b"X-XSS-Protection"] = b"1; mode=block"

        # Referrer-Policy
        if self.referrer_policy:
            headers[b"Referrer-Policy"] = self.referrer_policy.encode()

        # Permissions-Policy (formerly Feature-Policy)
        headers[b"Permissions-Policy"] = b"geolocation=(), microphone=(), camera=()"

        return headers

    async def __call__(self, scope: dict, receive: Callable, send: Callable, app: Callable):
        """Process request through security headers middleware."""
        if scope["type"] != "http":
            return await app(scope, receive, send)

        # Add security headers to response
        async def send_with_security(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))

                # Add security headers
                security_headers = self._get_security_headers()
                for name, value in security_headers.items():
                    headers.append((name, value))

                message["headers"] = headers

            await send(message)

        await app(scope, receive, send_with_security)
