from typing import Dict

from fastapi import APIRouter, HTTPException, Depends
from tinydb import TinyDB

from app.crud.form_crud import (
    create_form,
    get_form_by_name,
    get_all_forms,
    delete_form_by_name
)
from app.database import get_db
from app.schemas.form_schema import FormSchema
from app.services.form_service import find_matching_form

router = APIRouter(prefix="/forms", tags=["forms"])


@router.post("/get_form")
async def get_form_endpoint(data: Dict[str, str], db: TinyDB = Depends(get_db)):
    if not data:
        raise HTTPException(status_code=400, detail="No form data provided")

    matching_template = find_matching_form(data, db)

    return matching_template


@router.post("/", response_model=FormSchema)
async def create_form_endpoint(form_data: FormSchema, db: TinyDB = Depends(get_db)):
    try:
        return create_form(form_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{name}", response_model=FormSchema)
async def get_form_by_name_endpoint(name: str, db: TinyDB = Depends(get_db)):
    result = get_form_by_name(name, db)
    if not result:
        raise HTTPException(status_code=404, detail="Форма не найдена.")
    return result


@router.get("/", response_model=list[FormSchema])
async def get_all_forms_endpoint(db: TinyDB = Depends(get_db)):
    return get_all_forms(db)


@router.delete("/{name}")
async def delete_form_endpoint(name: str, db: TinyDB = Depends(get_db)):
    try:
        delete_form_by_name(name, db)
        return {"detail": "Форма удалена."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
