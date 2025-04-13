from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix="/file", tags=["File Upload Service"])


@router.post("/upload-file")
def upload_file(file: UploadFile):
    return {
        "name": file.filename,
        "type": file.content_type,
        "size_in_bytes": file.size,
    }
