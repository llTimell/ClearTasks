from fastapi import FastAPI
from app.auth import auth_router
from app.tasks import tasks_router
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

app.include_router(auth_router, prefix= "/auth") #router of authentication
app.include_router(tasks_router, prefix="/tasks")# router of tasks management

# Allow all origins 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict methods if needed
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"2550911-2487080 CLOUD PROJECT!"}