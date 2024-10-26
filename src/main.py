from fastapi import FastAPI

from src.db import engine
from src.models import Base
from src.routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return "Congratulation! Server still works!"
