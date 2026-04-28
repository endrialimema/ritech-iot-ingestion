from fastapi import FastAPI
from app.api.router import api_router
from app.core.middleware import rate_limit_middleware

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.middleware("http")(rate_limit_middleware)


@app.get("/health")
def health():
    return {"status": "ok"}
