from fastapi import APIRouter, FastAPI

from lavoro_applicant_api.database import db
from lavoro_applicant_api.routers.gateway import router as gateway_router


router = APIRouter(prefix="/api/v1")
router.include_router(gateway_router)

app = FastAPI()
app.include_router(router)
