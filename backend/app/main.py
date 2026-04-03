from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.knowledge import router as knowledge_router
from app.api.reports import router as reports_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)
print("CORS ORIGINS:", settings.allowed_origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(knowledge_router, prefix=settings.api_v1_prefix)
app.include_router(reports_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health",
    }
