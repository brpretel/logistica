from fastapi import Request

class Dia_Form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.dia: int
        self.usuario: str

    async def create_dia_form(self):
        form = await self.request.form()
        self.dia = form.get("dia")
        self.usuario = form.get("usuario")