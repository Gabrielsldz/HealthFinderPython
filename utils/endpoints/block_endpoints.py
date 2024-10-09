from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class BlockEndpointsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.app.state.is_updating_database:
            return JSONResponse(
                status_code=503,
                content={"detail": "Service Unavailable: Database update in progress"}
            )

        response = await call_next(request)
        return response
