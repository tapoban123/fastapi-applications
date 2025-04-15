from pydantic import BaseModel, AfterValidator
from typing import Annotated
from fastapi import HTTPException, status


def is_phone_number(number: int):
    if len(str(number)) == 10:
        return number
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Phone number must not be less than or greater than 10 digits.")


class ContactsBase:
    access_token: str
    name: str
    phone_number: Annotated[int, AfterValidator(is_phone_number)]
    country_code: str
    description: str | None


class CreateNewContact(BaseModel, ContactsBase):
    pass


class UpdateExistingContact(BaseModel, ContactsBase):
    contact_id: str


class UpdatedContactResponse(BaseModel):
    contact_id: str
    name: str
    phone_number: int
    country_code: str
    description: str | None
