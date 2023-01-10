from fastapi import APIRouter, Depends,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from managers.usuario import UserManager
from schemas.request.usuario import UserLoginIn, UserRegisterIn
from managers.auth import oauth2_scheme, is_master

router = APIRouter(tags=["Auth"])

"""
Registra un usuario en la base de datos y retorna el token, solo puede ser ejecutada por usuarios master
"""
@router.post("/register/", status_code=201 , dependencies=[Depends(oauth2_scheme),Depends(is_master)])
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.dict())
    return {"token": token}


@router.get("/login/")
async def login(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})
"""
Da login al usuario y retorna el token para mantener al usuario en sesion
"""
@router.post("/login/", status_code=201)
async def login(user_data: UserLoginIn):
    token = await UserManager.login(user_data.dict())
    return {"token": token}
