from fastapi import FastAPI
from auth.auth import router
import database.models as db_models
from database.config import engine

app = FastAPI()
app.include_router(router)

db_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return "Welcome to Contacts Management System with FastAPI"
