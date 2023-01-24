from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette import status
from managers.auth import AuthManager
from managers.master import MasterManager
from schemas.request.dias import DiasModel
from schemas.request.dias_distribuidor import Dia_Form
from schemas.request.productos import ProductForm
from schemas.request.productos_distribuidor import Product_user_Form
from schemas.request.usuario import RegisterForm, ModifyUserForm

router = APIRouter(prefix="/master",
                   tags=["master"],
                   responses={401: {"user": "Not authorized"}}
                   )

templates = Jinja2Templates(directory="front/static/templates")

"""@router.post("/register_Master/", status_code=201)
async def register_master(contraseña: int, user_data: UserRegisterMaster):
    token = await MasterManager.register_master(contraseña, user_data.dict())
    return {"token": token}"""


@router.post("/create_dia/")
async def create_dia(dia_data: DiasModel):
    return await MasterManager.create_dia(dia_data.dict())


# Confirma al master en sesion y dirige al template para agregar un usuario
@router.get("/register_user", response_class=HTMLResponse)
async def register_user(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("añadir_usuario.html", {"request": request, "user": user})


# Post para agregar un usuario
@router.post("/register_user", response_class=HTMLResponse)
async def register_user(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    form = RegisterForm(request)
    await form.create_register_form()
    user_id, password, role = form.user_id, form.password, form.role
    user_data = {"user_id": user_id, "password": password, "role": role}
    new_user = await AuthManager.register(user_data)
    if new_user is None:
        msg = "El usuario ya Existe"
        return templates.TemplateResponse("añadir_usuario.html", {"request": request, "msg": msg, "user": user})
    return RedirectResponse(url="/master/users", status_code=status.HTTP_302_FOUND)


@router.get("/create_product/", response_class=HTMLResponse)
async def create_product(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add_product.html", {"request": request, "user": user})


@router.post("/create_product/", response_class=HTMLResponse)
async def create_product(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    form = ProductForm(request)
    await form.create_product_form()
    nombre, categoria = form.nombre, form.categoria
    product_data = {"nombre": nombre, "categoria": categoria}
    producto = await MasterManager.create_product(product_data)
    if producto is None:
        msg = "El producto ya Existe"
        return templates.TemplateResponse("add_product.html", {"request": request, "msg": msg, "user": user})
    return RedirectResponse(url="/master/products", status_code=status.HTTP_302_FOUND)


@router.get("/products", response_class=HTMLResponse)
async def products(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    products = await MasterManager.get_all_products()
    return templates.TemplateResponse("products_list.html", {"request": request, "user": user, "products": products})

@router.get("/users", response_class=HTMLResponse)
async def users(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    users = await MasterManager.get_all_users()
    return templates.TemplateResponse("users_list.html", {"request": request, "user": user, "users": users})


@router.get("/edit_user/{user_id}", response_class=HTMLResponse)
async def edit_user(request: Request, user_id: int):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    modify_user, dias, productos = await MasterManager.get_user_for_update(user_id)
    dias_dis,produc_dist = await MasterManager.get_user_products_and_days(user_id)

    return templates.TemplateResponse("edit_user.html",
                                      {"request": request, "user": user, "modify_user": modify_user, "dias": dias,
                                       "productos": productos, "produc_dist":produc_dist, "dias_dis":dias_dis})


@router.post("/edit_user/")
async def modify_user(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    form = ModifyUserForm(request)
    await form.create_modify_user_form()
    role, status_user, user_id = form.role, form.status, form.user
    user_data = {"role": role, "status": status_user, "user_id": user_id}
    update = await MasterManager.update_user(user_data)
    if update is None:
        return RedirectResponse(url=f"/master/edit_user/{user_id}", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/master/users", status_code=status.HTTP_302_FOUND)

@router.post("/dias_distribuidor/")
async def create_dias_for_distribuidor(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    form = Dia_Form(request)
    await form.create_dia_form()
    dia, usuario = int(form.dia), int(form.usuario)
    dia_data = {"dia": dia, "usuario": usuario}
    update = await MasterManager.create_dia_for_distribuidor(dia_data)
    if update is None:
        msg = "Algo raro ocurrio verifica la informacion ingresada"
        return templates.TemplateResponse("edit_user.html", {"request": request, "msg": msg, "user": user})
    return RedirectResponse(url=f"/master/edit_user/{update['usuario']}", status_code=status.HTTP_302_FOUND)

@router.post("/assign_product/")
async def create_product_for_distribuidor(request: Request):
    user = await AuthManager.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    form = Product_user_Form(request)
    await form.create_product_for_user_form()
    producto, usuario = int(form.producto), int(form.usuario)
    product_data = {"producto": producto, "usuario": usuario}
    update = await MasterManager.post_product_for_user(product_data)
    if update is None:
        msg = "Algo raro ocurrio verifica la informacion ingresada"
        return templates.TemplateResponse("edit_user.html", {"request": request, "msg": msg, "user": user})
    return RedirectResponse(url=f"/master/edit_user/{update['usuario']}", status_code=status.HTTP_302_FOUND)






