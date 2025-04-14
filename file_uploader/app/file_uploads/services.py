import cloudinary
import cloudinary.uploader
from ..auth.services import is_token_valid
from fastapi import UploadFile
from ..database.core import db_dependency
from ..entities.file_data import UserFiles
from utils import *
import uuid
from ..exceptions import AccessTokenInvalidError, FileSizeMoreThan5MBError

from enums import ENV_VALUES

# Configuration
cloudinary.config(
    cloud_name=ENV_VALUES.CLOUDINARY_CLOUD_NAME.value,
    api_key=ENV_VALUES.CLOUDINARY_API_KEY.value,
    api_secret=ENV_VALUES.CLOUDINARY_API_SECRET.value,
    secure=True
)


def upload_file(token: str,
                file_name: str,
                description: str,
                file: UploadFile, db: db_dependency):
    user = is_token_valid(token, db)

    if not user:
        raise AccessTokenInvalidError()

    if not is_file_within_5mb(file.size):
        print(file.size)
        raise FileSizeMoreThan5MBError()

    upload_result = cloudinary.uploader.upload(file.file, asset_folder=f"/{user.id}/assets", public_id=file_name)

    file_data = UserFiles(
        id=uuid.uuid4().hex,
        user_id=user.id,
        name=file_name,
        description=description,
        url=upload_result["secure_url"],
        file_type=file.content_type,
        size=file.size,
    )

    db.add(file_data)
    db.commit()

    return {"details": "success"}


def fetch_all_files(token: str, db: db_dependency):
    user = is_token_valid(token, db)

    if not user:
        raise AccessTokenInvalidError()

    user_files = db.query(UserFiles).filter(UserFiles.user_id == user.id).all()

    return {
        "uid": user.id,
        "data": user_files
    }
