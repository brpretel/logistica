from fastapi import APIRouter
from starlette import status
from datetime import datetime
import pytz
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from managers.auth import AuthManager
from managers.disponibilidad import DisponibilidadManager
from models import RoleType
from schemas.request.disponibilidad import DisponibilidadForm

router = APIRouter(prefix="/disponibilidad",
                   tags=["disponibilidad"],
                   responses={401: {"user": "Not authorized"}}
                   )
templates = Jinja2Templates(directory="front/static/templates")


# Si es master dirige al Dashboard y si es distribuidor dirige al panel de disponibilidades
@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    elif user["role"] == RoleType.master:
        colombia_tz = pytz.timezone('America/Bogota')
        fecha = datetime.now(colombia_tz).date()

        disponibilidad, usuarios, cantidad_usuarios_activos, cantidad_dispos, cant_productos = await DisponibilidadManager.get_disponibilidades(
            user)
        return templates.TemplateResponse("dashboard_master.html",
                                          {"request": request, "disponibilidad": disponibilidad, "user": user,
                                           "usuarios": usuarios, "cantidad_usuarios_activos": cantidad_usuarios_activos,
                                           "cantidad_dispos": cantidad_dispos, "cant_productos": cant_productos,
                                           "fecha": fecha})
    disponibilidad, dias, date, productos, cant_dispos, cant_dias = await DisponibilidadManager.get_disponibilidades(
        user)
    return templates.TemplateResponse("disponibilidades_distribuidor.html",
                                      {"request": request, "disponibilidad": disponibilidad, "user": user, "dias": dias,
                                       "date": date, "productos": productos, "cant_dispos": cant_dispos,
                                       "cant_dias": cant_dias})

# Optione los datos necesarios para hacer el post de la disponibilidad
@router.get("/create/", response_class=HTMLResponse)
async def create_disponibilidad(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    dias, productos = await DisponibilidadManager.get_data_for_disponibiliad(user)
    return templates.TemplateResponse("add_disponibilidad.html", {"request": request, "user": user, "dias": dias, "productos":productos})


@router.post("/create/", response_class=HTMLResponse)
async def create_disponibilidad(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    form = DisponibilidadForm(request)
    await form.create_disponibilidad_form()
    producto, unidad, cantidad, dia_de_disponibilidad = form.producto,form.unidad, int(form.cantidad), form.dia_de_disponibilidad
    partes = producto.split("-")
    parte_1 = partes[0]
    parte_2 = partes[1]
    colombia_tz = pytz.timezone('America/Bogota')
    fecha = datetime.now(colombia_tz).date()
    disp_data = {"producto": parte_1, "categoria": parte_2,"cantidad": cantidad, "unidad": unidad, "fecha_de_creacion":fecha, "fecha_de_modificacion": fecha, "dia_de_disponibilidad":dia_de_disponibilidad}
    new_disp = await DisponibilidadManager.create_disponibilidad(disp_data, user)
    if new_disp is None:
        msg = "Algo raro ocurrio verifica la informacion ingresada"
        return templates.TemplateResponse("añadir_usuario.html", {"request": request, "msg": msg, "user": user})
    return RedirectResponse(url="/disponibilidad", status_code=status.HTTP_302_FOUND)



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
