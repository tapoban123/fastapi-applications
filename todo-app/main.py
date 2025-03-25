from fastapi import FastAPI
import models.db_models as db_models
from database import engine
from routes.route import router


app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Home"])
def home():
    return "Welcome to FastAPI To-Do Application."

app.include_router(router)