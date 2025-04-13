from fastapi import FastAPI
from .auth import controller as auth_controller
from .file_uploads import controller as file_controller
from .database import core
from .entities import file_data, user  # Importing to register them

core.Base.metadata.create_all(bind=core.engine)


app = FastAPI()
app.include_router(auth_controller.router)
app.include_router(file_controller.router)


@app.get("/")
def home():
    return "Welcome to File Uploader App.\nThis application allows the user to upload any file and retrieve them anytime."
