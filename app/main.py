from fastapi import FastAPI
from app.route.generator_route import router

app = FastAPI()

app.include_router(router)