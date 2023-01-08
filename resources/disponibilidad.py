from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import oauth2_scheme
from managers.disponibilidad import DisponibilidadManager
from schemas.request.disponibilidad import DisponibilidadModel
from schemas.response.disponibilidad import DisponibilidadOut

router = APIRouter(tags=["Disponibilidad"])


@router.get("/ordenes/", dependencies=[Depends(oauth2_scheme)], response_model=List[OrderOut])
async def get_orders(request: Request):
    user = request.state.user
    return await OrderManager.get_orders(user)


@router.post("/ordenes/", dependencies=[Depends(oauth2_scheme)], response_model=OrderOut)
async def create_order(orden: OrderModel, request: Request):
    user = request.state.user
    return await OrderManager.create_order(orden.dict(), user)
