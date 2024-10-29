from fastapi import FastAPI

from src.db import engine
from src.models import Base
from src.routers.task import router as task_router
from src.routers.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)


@app.get("/")
def read_root():
    return "Congratulation! Server still works!"
