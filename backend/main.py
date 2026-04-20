from fastapi import FastAPI
from backend.database import Base, engine
from backend.routes import auth_routes, task_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(task_routes.router)