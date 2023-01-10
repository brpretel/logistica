from fastapi import APIRouter, Depends

from managers.auth import oauth2_scheme, is_master
from managers.master import MasterManager
from schemas.request.productos import ProductosModel
from schemas.request.usuario import UserRegisterMaster

router = APIRouter(tags=["Master"])


@router.post("/register_Master/", status_code=201)
async def register_master(contraseña: int, user_data: UserRegisterMaster):
    token = await MasterManager.register_master(contraseña, user_data.dict())
    return {"token": token}


@router.post("/create_product/", dependencies=[Depends(oauth2_scheme), Depends(is_master)])
async def create_product(product_data: ProductosModel):
    return await MasterManager.create_product(product_data.dict())
