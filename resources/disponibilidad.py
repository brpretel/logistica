from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import oauth2_scheme
from managers.disponibilidad import DisponibilidadManager
from schemas.request.disponibilidad import DisponibilidadModel, DisponibilidadUpdateModel
from schemas.response.disponibilidad import DisponibilidadOut

router = APIRouter(tags=["Disponibilidad"])



@router.get("/ordenes/", dependencies=[Depends(oauth2_scheme)], response_model=List[OrderOut])
async def get_orders(request: Request):
    user = request.state.user
    return await OrderManager.get_orders(user)


"""
Retorna las disponibilidades, dias de disponibilidad y los productos que pertenecen al usuario en sesion.
"""
@router.get("/disponibilidades/", dependencies=[Depends(oauth2_scheme)])
async def get_data_for_distribuidor(request: Request):
    user_id = request.state.user
    disponibilidades, disp_dias_de_distribuidores = await DisponibilidadManager.get_data_for_distribuidor(user_id)
    return {"disponibilidades": disponibilidades, "disp_dias_de_distribuidores": disp_dias_de_distribuidores}

@router.post("/ordenes/", dependencies=[Depends(oauth2_scheme)], response_model=OrderOut)
async def create_order(orden: OrderModel, request: Request):
    user = request.state.user
    return await OrderManager.create_order(orden.dict(), user)
