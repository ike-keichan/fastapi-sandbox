from fastapi import FastAPI

from api.routers.hello import index as hello
from api.routers.task import index as task

app = FastAPI()

app.include_router(hello.router)
app.include_router(task.router)
