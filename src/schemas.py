from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class ContactModel(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=20)
    birthday: date | None = Field(None)
    additional_info: str | None = Field(None, max_length=255)

    model_config = ConfigDict(from_attributes=True)


class ContactUpdate(ContactModel):
    pass


class ContactResponse(ContactModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
