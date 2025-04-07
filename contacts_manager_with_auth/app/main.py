from fastapi import FastAPI
from .auth import auth_routes
from .contacts_services import contacts_services
from .database import models
from .database.config import engine

app = FastAPI()
app.include_router(auth_routes.router)
app.include_router(contacts_services.router)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return "Welcome to Contacts Management System with FastAPI"
