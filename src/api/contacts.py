from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactResponse, ContactModel, ContactUpdate
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
        skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip, limit)
    return contacts

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    first_name: str = None, last_name: str = None, email: str = None, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contacts = await contact_service.search_contacts(first_name, last_name, email)
    return contacts


@router.get("/upcoming_birthday", response_model=List[ContactResponse])
async def get_contacts_upcoming_birthday(db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts_upcoming_birthday()
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_note(
        body: ContactUpdate, contact_id: int, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    note = await contact_service.update_contact(contact_id, body)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return note


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_note(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact