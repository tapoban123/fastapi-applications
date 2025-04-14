from pydantic import BaseModel


class UploadFileData(BaseModel):
    file_name: str
    description: str | None
