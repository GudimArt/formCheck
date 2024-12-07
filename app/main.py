from fastapi import FastAPI

from app.routers.form_router import router as form_router

app = FastAPI()

app.include_router(form_router)
