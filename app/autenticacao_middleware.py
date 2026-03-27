from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class AuthenticationToken(BaseHTTPMiddleware):
    """
    Middleware simples de autenticação por cookie.

    Regras:
    - Rotas públicas passam sem autenticação.
    - Rotas protegidas exigem a existência do cookie `session_token`.
    - Para rotas API (`/api/*`) retorna 401; para páginas HTML faz redirect para `/login`.
    """

    # Rotas e prefixos que não precisam de autenticação.
    _PUBLIC_PATHS = {
        "/",
        "/login",
        "/registro",
        "/logout",
    }
    _STATIC_PREFIX = "/static"
    _OPENAPI_PREFIX = "/openapi.json"
    _DOCS_PREFIXES = ("/docs", "/redoc")

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        path_normalized = self._normalize_path(path)

        if self._should_bypass_auth(path, path_normalized):
            return await call_next(request)

        # Autenticação exigida para qualquer rota que não seja explicitamente pública.
        token = request.cookies.get("session_token")
        if not token:
            # Evita redirect em chamadas de API (fetch/XHR).
            return self._unauthenticated_response(request)

        return await call_next(request)

    @staticmethod
    def _normalize_path(path: str) -> str:
        # Mantém a checagem consistente: "/login/" vira "/login".
        return path.rstrip("/") or "/"

    def _should_bypass_auth(self, path: str, path_normalized: str) -> bool:
        return (
            path_normalized in self._PUBLIC_PATHS
            or path.startswith(f"{self._STATIC_PREFIX}/")
            or path == self._STATIC_PREFIX
            or path.startswith(self._OPENAPI_PREFIX)
            or any(path.startswith(prefix) for prefix in self._DOCS_PREFIXES)
        )

    def _unauthenticated_response(self, request: Request):
        path = request.url.path
        is_api = path.startswith("/api/") or path.startswith("/api")

        if is_api:
            return JSONResponse(
                status_code=401,
                content={"detail": "Não autenticado. Faça login."},
            )

        return RedirectResponse(url="/login", status_code=303)
