from typing import Optional
from fastapi import Request
from models import RoleType, UserStatus


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("user_id")
        self.password = form.get("password")


class RegisterMasterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.codigo: str = None
        self.user_id: str = None
        self.password: str = None
        self.role: RoleType = None

    async def create_register_master_form(self):
        form = await self.request.form()
        self.codigo = form.get("codigo")
        self.user_id = form.get("user_id")
        self.password = form.get("password")
        self.role = form.get("role")

class RegisterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.user_id: str = None
        self.password: str = None
        self.role: RoleType = None

    async def create_register_form(self):
        form = await self.request.form()
        self.user_id = form.get("user_id")
        self.password = form.get("password")
        self.role = form.get("role")


class ModifyUserForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.user: str
        self.role: RoleType = None
        self.status: UserStatus = None

    async def create_modify_user_form(self):
        form = await self.request.form()
        self.user = form.get("usuario")
        self.role = form.get("role")
        self.status = form.get("status")
