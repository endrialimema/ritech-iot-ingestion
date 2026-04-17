from fastapi import FastAPI
from .api.router import api_router
from .core.middleware import rate_limit_middleware

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.middleware("http")(rate_limit_middleware)