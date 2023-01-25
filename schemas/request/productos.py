from fastapi import Request


class ProductForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.nombre: str = None
        self.categoria: str = None

    async def create_product_form(self):
        form = await self.request.form()
        self.nombre = form.get("nombre")
        self.categoria = form.get("categoria")
