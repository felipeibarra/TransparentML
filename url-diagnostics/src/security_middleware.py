"""
Security Headers Middleware
============================
Implements comprehensive HTTP security headers to protect against common web vulnerabilities.

Headers implemented:
- Content-Security-Policy (CSP): Prevents XSS attacks
- X-Frame-Options: Prevents clickjacking
- Strict-Transport-Security (HSTS): Forces HTTPS
- X-Content-Type-Options: Prevents MIME sniffing
- X-XSS-Protection: Legacy XSS protection
- Referrer-Policy: Controls referrer information
- Permissions-Policy: Restricts browser features
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import os


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all HTTP responses.
    
    This middleware adds multiple security headers recommended by OWASP
    to protect against common web vulnerabilities like XSS, clickjacking,
    MIME sniffing, and more.
    """
    
    def __init__(self, app: ASGIApp, enable_hsts: bool = False):
        """
        Initialize security middleware.
        
        Args:
            app: ASGI application
            enable_hsts: Enable Strict-Transport-Security (only in production with HTTPS)
        """
        super().__init__(app)
        self.enable_hsts = enable_hsts or os.getenv("ENABLE_HSTS", "false").lower() == "true"
    
    async def dispatch(self, request, call_next):
        """Process request and add security headers to response."""
        response = await call_next(request)
        
        # Content Security Policy (CSP)
        # Prevents XSS attacks by controlling which resources can be loaded
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' http://localhost:* ws://localhost:* http://127.0.0.1:*; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        
        # X-Frame-Options: Prevents clickjacking attacks
        # DENY: Page cannot be displayed in frame/iframe
        response.headers["X-Frame-Options"] = "DENY"
        
        # Strict-Transport-Security (HSTS)
        # Forces browsers to use HTTPS (only enable in production with valid SSL)
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # X-Content-Type-Options: Prevents MIME sniffing
        # Ensures browsers respect the declared Content-Type
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # X-XSS-Protection: Legacy XSS protection for older browsers
        # Modern browsers rely on CSP, but this helps with older ones
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer-Policy: Controls how much referrer information is sent
        # strict-origin-when-cross-origin: Send full URL for same-origin, origin only for cross-origin
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions-Policy: Restricts browser features
        # Disables geolocation, microphone, and camera access
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=()"
        )
        
        # X-Permitted-Cross-Domain-Policies: Restricts Adobe Flash/PDF cross-domain policies
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        
        # Cache-Control for HTML responses (prevent caching sensitive data)
        if "text/html" in response.headers.get("content-type", ""):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
        
        return response


class CORSConfig:
    """
    CORS Configuration for different environments.
    
    In development, we allow localhost origins.
    In production, only allow specific domains.
    """
    
    @staticmethod
    def get_allowed_origins():
        """Get allowed origins based on environment."""
        env = os.getenv("ENVIRONMENT", "development")
        
        if env == "production":
            # Production: Only allow specific domains
            return [
                "https://transparentml.yourdomain.com",
                "https://www.transparentml.yourdomain.com"
            ]
        else:
            # Development: Allow localhost on common ports
            return [
                "http://localhost:8003",
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:8003",
                "http://127.0.0.1:3000"
            ]
    
    @staticmethod
    def get_cors_config():
        """Get complete CORS configuration."""
        return {
            "allow_origins": CORSConfig.get_allowed_origins(),
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": [
                "Accept",
                "Accept-Language",
                "Content-Type",
                "Authorization",
                "X-Requested-With",
                "X-Request-ID"
            ],
            "expose_headers": [
                "Content-Length",
                "X-Request-ID",
                "X-RateLimit-Limit",
                "X-RateLimit-Remaining"
            ],
            "max_age": 600  # Cache preflight requests for 10 minutes
        }


def get_security_report():
    """
    Generate security configuration report.
    
    Returns:
        dict: Security configuration status
    """
    return {
        "security_headers": {
            "content_security_policy": "enabled",
            "x_frame_options": "DENY",
            "x_content_type_options": "nosniff",
            "x_xss_protection": "1; mode=block",
            "referrer_policy": "strict-origin-when-cross-origin",
            "permissions_policy": "restricted",
            "hsts_enabled": os.getenv("ENABLE_HSTS", "false").lower() == "true"
        },
        "cors": {
            "environment": os.getenv("ENVIRONMENT", "development"),
            "allowed_origins": CORSConfig.get_allowed_origins(),
            "allow_credentials": True
        },
        "recommendations": [
            "Enable HSTS in production with valid SSL certificate",
            "Regularly audit CSP policy for XSS vulnerabilities",
            "Consider implementing rate limiting",
            "Add authentication/authorization for sensitive endpoints"
        ]
    }
