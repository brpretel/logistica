from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from managers.auth import AuthManager
from managers.disponibilidad import DisponibilidadManager

router = APIRouter(prefix="/disponibilidad",
                   tags=["disponibilidad"],
                   responses={401: {"user": "Not authorized"}}
                   )
templates = Jinja2Templates(directory="front/static/templates")

"""
Retorna las disponibilidades, dias de disponibilidad y los productos que pertenecen al usuario en sesion.
"""


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    disponibilidades, disp_dias_de_distribuidores = await DisponibilidadManager.get_data_for_distribuidor(user)
    return templates.TemplateResponse("dashboard.html", {"request": request,"disponibilidades": disponibilidades, "disp_dias": disp_dias_de_distribuidores})


"""@router.get("/disponibilidades/")
async def get_data_for_distribuidor(user: dict = Depends(AuthManager.get_current_user)):
    if user is None:
        print("Error")
    disponibilidades, disp_dias_de_distribuidores = await DisponibilidadManager.get_data_for_distribuidor(user)
    return {"disponibilidades": disponibilidades, "disp_dias": disp_dias_de_distribuidores}"""


"""
Retorna la dosponibilidad creada por el usuario.
"""


"""@router.post("/disponibilidades/", response_model=DisponibilidadOut)
async def create_disponibilidad(disponibilidad: DisponibilidadModel, request: Request):
    user = request.state.user
    return await DisponibilidadManager.create_disponibilidad(disponibilidad.dict(), user)"""


"""
Retorna la disponibilidad actualizada con los nuevos datos.
"""


"""@router.post("/disponibilidad/{disponibilidad_id}/")
async def update_disponibilidad(disponibilidad_id: int, disponibilidad: DisponibilidadUpdateModel, request: Request):
    user = request.state.user
    disponibilidad.status = "modificado"
    return await DisponibilidadManager.update_disponibilidad(disponibilidad_id, disponibilidad.dict(), user)"""
