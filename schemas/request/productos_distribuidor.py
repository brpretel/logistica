from fastapi import Request


class Product_user_Form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.producto: str = None
        self.usuario: str = None

    async def create_product_for_user_form(self):
        form = await self.request.form()
        self.producto = form.get("producto")
        self.usuario = form.get("usuario")
