import os
import sys

# Ensure the 'src' directory containing the 'app' package is always in sys.path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
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
    candidate_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'index.html')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'index.html')),
        os.path.abspath(os.path.join(os.getcwd(), 'index.html')),
    ]
    for index_path in candidate_paths:
        if os.path.exists(index_path):
            return FileResponse(index_path)
    return JSONResponse({"message": f"{settings.PROJECT_NAME} API is running", "docs": "/docs"})
