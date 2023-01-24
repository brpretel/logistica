from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from db import database
from resources.routes import api_router

app = FastAPI()
app.include_router(api_router)
app.mount("/front/static", StaticFiles(directory="front/static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



