from pydantic import BaseModel


class UpdateFileData(BaseModel):
    resource_id: str
    new_asset_name: str | None
    new_description: str | None
