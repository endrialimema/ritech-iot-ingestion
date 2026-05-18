from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # allowes frontend requests from different origins
from app.api.router import api_router
from app.core.middleware import rate_limit_middleware

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # any origin can access the API
    allow_methods=["GET", "POST"], # only these HTTP methods are allowed
    allow_headers=["*"], # any HTTP headers are allowed
)

app.include_router(api_router, prefix="/api/v1")
app.middleware("http")(rate_limit_middleware)


@app.get("/health")
def health():
    return {"status": "ok"}
