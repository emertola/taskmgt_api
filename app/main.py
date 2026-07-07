from fastapi import FastAPI

from app.routers.tasks import router as tasks_router
from app.core.config import settings

app = FastAPI(
  title=settings.app_name
)

app.include_router(tasks_router)

