from fastapi import FastAPI

from app import __app_name__, __version__
from app.api.router import api_router

app = FastAPI(
    title=__app_name__,
    description="REST API for the NexusAI enterprise AI knowledge platform.",
    version=__version__,
)

app.include_router(api_router)
