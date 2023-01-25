from fastapi import APIRouter
from resources import auth, disponibilidad, master

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(disponibilidad.router)
api_router.include_router(master.router)