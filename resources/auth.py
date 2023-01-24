from fastapi import APIRouter, Depends,Request, Response, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from managers.auth import AuthManager
from starlette import status
from schemas.request.usuario import LoginForm, RegisterForm, RegisterMasterForm
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   responses={401:{"user":"Not authorized"}}
                   )

templates = Jinja2Templates(directory="front/static/templates")


@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await AuthManager.authenticate_user(form_data.username, form_data.password)
    if not user:
        return False
    token_expires = timedelta(minutes=120)
    token = AuthManager.create_access_token(user,expires_delta=token_expires)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})


@router.post("/", response_class=HTMLResponse)
async def login(request:Request):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/disponibilidad", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form)
        if not validate_user_cookie:
            msg = "Contraseña Incorrecta o Usuario desactivado"
            return templates.TemplateResponse("login.html", {"request":request, "msg":msg})
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request":request, "msg":msg})

@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response

@router.get("/register_master", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("register_master.html", {"request": request})


@router.post("/register_master", response_class=HTMLResponse)
async def register_user(request: Request):
    form = RegisterMasterForm(request)
    await form.create_register_master_form()
    codigo,user_id, password, role = form.codigo,form.user_id, form.password, form.role
    if codigo == "mrspecialties123":
        user_data = {"user_id": user_id, "password": password, "role": role}
        new_user = await AuthManager.register(user_data)
        if new_user is None:
            msg = "El usuario ya Existe"
            return templates.TemplateResponse("register_master.html", {"request": request, "msg": msg})
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    msg = "contraseña incorrecta"
    return templates.TemplateResponse("register_master.html", {"request": request, "msg":msg})