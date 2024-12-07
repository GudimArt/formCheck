from typing import Dict

from fastapi import Depends
from tinydb import TinyDB

from app.database import get_db
from app.utils.validation import is_valid_phone, is_valid_date, is_valid_email, is_valid_text


def detect_field_type(value: str) -> str:
    if is_valid_email(value):
        return "email"
    elif is_valid_phone(value):
        return "phone"
    elif is_valid_date(value):
        return "date"
    elif is_valid_text(value):
        return "text"
    return "unknown"


def find_matching_form(data: Dict[str, str], db: TinyDB = Depends(get_db)) -> str | Dict[str, str]:
    templates = db.table('forms').all()

    for template in templates:
        form_name = template.pop("form_name")
        mismatched_fields = {}

        for field_name, value in data.items():
            actual_type = detect_field_type(data[field_name])
            if field_name not in template:
                mismatched_fields[field_name] = actual_type
                continue
            elif field_name in template:
                if template[field_name] != actual_type:
                    mismatched_fields[field_name] = actual_type
                    continue
        if not mismatched_fields:
            return form_name

    return {field: detect_field_type(type_) for field, type_ in data.items()}
