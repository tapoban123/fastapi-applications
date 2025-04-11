from fastapi import FastAPI
from .auth import services

app = FastAPI()
app.include_router(services.router)


@app.get("/")
def home():
    return "Welcome to File Uploader App.\nThis application allows the user to upload any file and retrieve them anytime."
