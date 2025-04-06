from fastapi import FastAPI
from routers.auth import auth
from routers.contacts_services import contacts_services
import database.models as db_models
from database.config import engine

app = FastAPI()
app.include_router(auth.router)
app.include_router(contacts_services.router)

db_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return "Welcome to Contacts Management System with FastAPI"
