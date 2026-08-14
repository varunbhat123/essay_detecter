import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# When running from the repository root, ensure the backend package is importable.
if os.getcwd().endswith("backend"):
    package_root = os.getcwd()
else:
    package_root = os.path.join(os.getcwd(), "backend")
if package_root not in sys.path:
    sys.path.insert(0, package_root)

from app.core.config import settings
from app.routes.analyze import router as analyze_router
from app.routes.detect import router as detect_router
from app.routes.evaluate import router as evaluate_router
from app.routes.health import router as health_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API for the AI Essay Detector application.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(detect_router)
app.include_router(evaluate_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": settings.app_name, "status": "initialized"}
