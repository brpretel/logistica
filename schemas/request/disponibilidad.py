from fastapi import Request

class DisponibilidadForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.producto: str = None
        self.unidad: str = None
        self.cantidad: float = None
        self.dia_de_disponibilidad: str = None

    async def create_disponibilidad_form(self):
        form = await self.request.form()
        self.producto = form.get("producto")
        self.unidad = form.get("unidad")
        self.cantidad = form.get("cantidad")
        self.dia_de_disponibilidad = form.get("dia_de_disponibilidad")
