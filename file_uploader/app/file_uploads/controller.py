from fastapi import APIRouter, Header, Form, File
from typing import Annotated
from .models import UpdateFileData
from ..database.core import db_dependency
from .services import *

router = APIRouter(prefix="/file", tags=["File Upload Service"])


@router.post("/upload-file")
def upload_file_to_server(token: Annotated[str, Header(title="Enter auth token")],
                          db: db_dependency,
                          file_name: str = Form(...),
                          description: str = Form(...),
                          file: UploadFile = File(...),
                          ):
    return upload_file(token, file=file,
                       db=db,
                       file_name=file_name,
                       description=description)


@router.get("/fetch-files")
def fetch_all_files_of_user(token: Annotated[str, Header(title="Enter auth token")], db: db_dependency):
    return fetch_all_files(token, db)


@router.put("/update-asset")
def update_user_asset(token: Annotated[str, Header(title="Enter access token")],
                      new_file_data: UpdateFileData,
                      db: db_dependency):
    return update_asset(token,
                        resource_id=new_file_data.resource_id,
                        new_name=new_file_data.new_asset_name,
                        description=new_file_data.new_description,
                        db=db)


@router.delete("/delete-asset/{resource_id}")
def delete_user_asset(token: Annotated[str, Header(title="Enter access token")],
                      resource_id: str,
                      db: db_dependency):
    return delete_asset(
        db=db,
        token=token,
        resource_id=resource_id
    )
