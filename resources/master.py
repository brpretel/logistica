from typing import List
from fastapi import APIRouter, Depends
from starlette.requests import Request
from managers.disponibilidad import DisponibilidadManager
from managers.master import MasterManager
from schemas.request.dias import DiasModel
from schemas.request.productos import ProductosModel
from schemas.response.disponibilidad import DisponibilidadOut

router = APIRouter(tags=["Master"])


"""@router.post("/register_Master/", status_code=201)
async def register_master(contraseña: int, user_data: UserRegisterMaster):
    token = await MasterManager.register_master(contraseña, user_data.dict())
    return {"token": token}"""

@router.post("/create_product/")
async def create_product(product_data: ProductosModel):
    return await MasterManager.create_product(product_data.dict())

@router.post("/create_dia/")
async def create_product(dia_data: DiasModel):
    return await MasterManager.create_dia(dia_data.dict())


"""
Retorna todas las disponibilidades en la base de datos, solo puede ser usada por usuarios master.
"""
@router.get("/all_disponibilidades/", response_model=List[DisponibilidadOut])
async def get_all_disponibilidades(request: Request):
    user = request.state.user
    return await DisponibilidadManager.get_all_disponibilidades(user)
