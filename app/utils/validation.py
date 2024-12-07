import re
from datetime import datetime


def is_valid_phone(value: str) -> bool:
    return bool(re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", value))


def is_valid_date(value: str) -> bool:
    if re.match(r"^\d{2}\.\d{2}\.\d{4}$", value) or re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        try:
            if '.' in value:
                datetime.strptime(value, "%d.%m.%Y")
            elif '-' in value:
                datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return False


def is_valid_email(value: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value))


def is_valid_text(value: str) -> bool:
    return isinstance(value, str)
