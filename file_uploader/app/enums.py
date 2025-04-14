from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()


class ENV_VALUES(Enum):
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_ALGORITHM = os.environ.get("ALGORITHM")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUD_NAME")
