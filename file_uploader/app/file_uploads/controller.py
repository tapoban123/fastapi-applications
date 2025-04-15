from fastapi import APIRouter, Header, Form, File
from typing import Annotated
from .models import UploadFileData
from ..database.core import db_dependency
from .services import *

router = APIRouter(prefix="/file", tags=["File Upload Service"])


@router.post("/upload-file")
def upload_file_to_server(token: Annotated[str, Header(title="Enter auth token")],
                          db: db_dependency,
                          file_name: str = Form(...),
                          resource_id: str = Form(default=uuid.uuid4(),
                                                  min_length=1, ),
                          description: str = Form(...),
                          file: UploadFile = File(...),
                          ):
    return upload_file(token, file=file,
                       db=db,
                       resource_id=resource_id,
                       file_name=file_name,
                       description=description)


@router.get("/fetch-files")
def fetch_all_files_of_user(token: Annotated[str, Header(title="Enter auth token")], db: db_dependency):
    return fetch_all_files(token, db)
