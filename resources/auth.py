from fastapi import APIRouter, Depends

from managers.usuario import UserManager
from schemas.request.usuario import UserLoginIn, UserRegisterIn
from managers.auth import oauth2_scheme, is_master

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201 , dependencies=[Depends(oauth2_scheme),Depends(is_master)])
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.dict())
    return {"token": token}

@router.post("/login/", status_code=201)
async def login(user_data: UserLoginIn):
    token = await UserManager.login(user_data.dict())
    return {"token": token}
