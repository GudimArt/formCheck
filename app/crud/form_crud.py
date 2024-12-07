from fastapi import HTTPException, Depends
from tinydb import TinyDB, Query

from app.database import get_db
from app.schemas.form_schema import FormSchema


def create_form(form_data: FormSchema, db: TinyDB = Depends(get_db)) -> FormSchema:
    if db.table("forms").contains(Query().form_name == form_data.form_name):
        raise HTTPException(status_code=400, detail=f"Form with name {form_data.form_name} already exists.")

    form_entry = {"form_name": form_data.form_name,
                  **form_data.model_dump(exclude_unset=True)}
    db.table("forms").insert(form_entry)

    return form_data


def get_form_by_name(form_name: str, db: TinyDB = Depends(get_db)) -> FormSchema | None:
    result = db.table("forms").get(Query().form_name == form_name)
    if result:
        return FormSchema(**result)
    return None


def get_all_forms(db: TinyDB = Depends(get_db)) -> list[FormSchema]:
    results = db.table("forms").all()
    return [FormSchema(**entry) for entry in results]


def delete_form_by_name(form_name: str, db: TinyDB = Depends(get_db)) -> bool:
    if not db.table("forms").contains(Query().form_name == form_name):
        raise HTTPException(status_code=404, detail=f"Form with name {form_name} not found.")

    db.table("forms").remove(Query().form_name == form_name)
    return True
