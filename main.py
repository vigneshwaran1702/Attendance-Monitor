import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

ROOT_DIR = os.path.dirname(__file__)
BACKEND_SRC = os.path.join(ROOT_DIR, "attendance-system-v2", "backend", "src")
if BACKEND_SRC not in sys.path:
    sys.path.insert(0, BACKEND_SRC)

from app.core.config.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    index_path = os.path.join(ROOT_DIR, 'index.html')
    return FileResponse(index_path)
