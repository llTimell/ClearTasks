from fastapi import FastAPI
from app.auth import auth_router
from app.tasks import tasks_router

app= FastAPI()

app.include_router(auth_router, prefix= "/auth") #router of authentication
app.include_router(tasks_router, prefix="/tasks")# router of tasks management


@app.get("/")
def read_root():
    return {"2550911-2487080 CLOUD PROJECT!"}