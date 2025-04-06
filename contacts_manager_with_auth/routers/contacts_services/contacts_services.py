from fastapi import APIRouter, status
from routers.contacts_services.models import CreateNewContact, UpdateExistingContact

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_new_contact(token: str):
    return {"details": "contact created"}
