from fastapi import APIRouter, status, HTTPException
from .models import CreateNewContact, UpdateExistingContact, UpdatedContactResponse
from app.auth.auth_routes import validate_token
from ..database.config import db_dependency
from ..database.models import Contacts
import uuid

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_new_contact(contact_data: CreateNewContact, db: db_dependency):
    user_id = validate_token(contact_data.access_token, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not validated.")

    contact = Contacts(
        id=uuid.uuid4().hex,
        user_id=user_id,
        name=contact_data.name,
        contact_number=contact_data.phone_number,
        country_code=contact_data.country_code,
        description=contact_data.description,
    )
    db.add(contact)
    db.commit()

    return {"details": "success"}


@router.put("/update", response_model=UpdatedContactResponse)
def update_existing_contact(new_contact: UpdateExistingContact, db: db_dependency):
    user_id = validate_token(new_contact.access_token, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User.")

    contact = db.query(Contacts).filter(new_contact.contact_id == Contacts.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No contact found.")

    contact.name = new_contact.name
    contact.contact_number = new_contact.phone_number
    contact.country_code = new_contact.country_code
    contact.description = new_contact.description

    db.add(contact)
    db.commit()

    return new_contact.model_dump()


@router.get("/fetch-contacts")
def fetch_all_contacts(token: str, db: db_dependency):
    user_id = validate_token(token, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User validation failed.")

    contacts = db.query(Contacts).filter(user_id == Contacts.user_id).all()

    return contacts


@router.delete("/delete")
def delete_contact(token: str, contact_id: str, db: db_dependency):
    user_id = validate_token(token, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User validation failed.")

    db.query(Contacts).filter(contact_id == Contacts.id).delete()
    db.commit()

    return {"detail": "success"}
