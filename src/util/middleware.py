from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .auth_utils import decode_jwt_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public routes
        if request.url.path.startswith("/authenticate") or request.url.path.startswith("/static") or request.url.path.startswith("/"):
            return await call_next(request)

        # Check for JWT token in the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = auth_header.split(" ")[1]
        try:
            payload = decode_jwt_token(token)
            request.state.user = payload
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        response = await call_next(request)
        return response