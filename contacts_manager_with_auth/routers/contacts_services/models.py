from pydantic import BaseModel


class ContactsBase:
    name: str
    phone_number: int
    country_code: str
    description: str | None


class CreateNewContact(BaseModel, ContactsBase):
    pass


class UpdateExistingContact(BaseModel, ContactsBase):
    contact_id: str
