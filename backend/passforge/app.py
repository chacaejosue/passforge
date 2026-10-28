"""Flask application factory with security headers and rate limiting."""

from __future__ import annotations

import os
import threading
import time
from collections import deque

from flask import Flask, jsonify, request

from .routes import api


class SlidingWindowRateLimiter:
    """Thread-safe in-memory rate limiter per client IP."""

    def __init__(self, max_requests: int = 60, window_seconds: float = 60.0) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, key: str) -> tuple[bool, int]:
        if self.max_requests <= 0:
            return True, 0
        now = time.monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            bucket = self._hits.get(key)
            if bucket is None:
                bucket = deque()
                self._hits[key] = bucket
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            if len(bucket) >= self.max_requests:
                retry_after = max(1, int(self.window_seconds - (now - bucket[0])) + 1)
                return False, retry_after
            bucket.append(now)
            # Evict stale keys periodically to bound memory usage
            if len(self._hits) > 2048:
                stale_keys = [k for k, v in self._hits.items() if not v or v[-1] <= cutoff]
                for k in stale_keys:
                    self._hits.pop(k, None)
            return True, 0


def _client_ip() -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


def create_app(rate_limit_per_minute: int | None = None) -> Flask:
    app = Flask(__name__)
    configured_origins = os.getenv("FRONTEND_URL", "http://localhost:4321,http://127.0.0.1:4321")
    limit = (
        rate_limit_per_minute
        if rate_limit_per_minute is not None
        else int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    )
    limiter = SlidingWindowRateLimiter(max_requests=limit, window_seconds=60.0)

    app.config.from_mapping(
        MAX_CONTENT_LENGTH=16 * 1024,
        ALLOWED_ORIGINS={origin.strip() for origin in configured_origins.split(",") if origin.strip()},
        RATE_LIMITER=limiter,
    )
    app.register_blueprint(api, url_prefix="/api")

    @app.before_request
    def enforce_rate_limit():
        if request.path == "/api/passwords" and request.method == "POST":
            allowed, retry_after = limiter.is_allowed(_client_ip())
            if not allowed:
                response = jsonify(
                    error="Demasiadas solicitudes. Por favor, espera unos segundos antes de generar más contraseñas."
                )
                response.status_code = 429
                response.headers["Retry-After"] = str(retry_after)
                return response
        return None

    @app.after_request
    def add_security_and_cors_headers(response):
        # Read the request origin without adding credentials or wildcard access.
        origin = request.headers.get("Origin", "")
        if origin in app.config["ALLOWED_ORIGINS"]:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), interest-cohort=()"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        return response

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error="Ruta no encontrada."), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify(error="Método HTTP no permitido."), 405

    @app.errorhandler(413)
    def request_too_large(_error):
        return jsonify(error="La solicitud es demasiado grande."), 413

    @app.errorhandler(500)
    def internal_server_error(_error):
        return jsonify(error="Error interno del servidor."), 500

    return app


app = create_app()
