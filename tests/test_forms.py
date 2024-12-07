# tests/test_forms.py
import pytest
from fastapi.testclient import TestClient
from tinydb import TinyDB, Query

from app.main import app


@pytest.fixture
def db(tmp_path):
    db_file = tmp_path / "test_db.json"
    db = TinyDB(db_file)

    db.table("forms").insert({
        "form_name": "Order Form",
        "customer_email": "email",
        "customer_phone": "phone",
        "order_date": "date",
        "order_number": "text"
    })
    db.table("forms").insert({
        "form_name": "User Registration",
        "email": "email",
        "first_name": "text",
        "last_name": "text",
        "phone_number": "phone",
        "birthdate": "date"
    })

    yield db

    db.truncate()


@pytest.fixture
def client(db):
    from app.database import get_db
    app.dependency_overrides[get_db] = lambda: db
    client = TestClient(app)
    return client


def test_create_form(client, db):
    form_data = {
        "form_name": "New Form",
        "customer_email": "email",
        "customer_phone": "phone",
        "order_date": "date"
    }

    response = client.post("/forms/", json=form_data)

    assert response.status_code == 200
    assert response.json() == form_data

    forms_table = db.table("forms")
    form = forms_table.get(Query().form_name == "New Form")
    assert form is not None


def test_get_form_by_name(client, db):
    form_name = "Order Form"
    form_data = {
        "form_name": "Order Form",
        "customer_email": "email",
        "customer_phone": "phone",
        "order_date": "date",
        "order_number": "text"
    }

    response = client.get(f"/forms/{form_name}")

    assert response.status_code == 200
    assert response.json() == form_data


def test_get_all_forms(client, db):
    response = client.get("/forms/")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_delete_form_by_name(client, db):
    form_name = "Order Form"

    response = client.delete(f"/forms/{form_name}")
    assert response.status_code == 200

    forms_table = db.table("forms")
    form = forms_table.get(Query().form_name == form_name)
    assert form is None


def test_find_matching_form(client, db):
    data = {
        "customer_email": "ffff@mail.com",
        "customer_phone": "+7 900 802 33 33",
        "order_date": "22.12.2015"
    }

    response = client.post("/forms/get_form/", json=data)

    assert response.status_code == 200
    assert response.json() == "Order Form"


def test_find_matching_form_with_mismatched_fields(client, db):
    data = {
        "customer_email": "ffff@mail.com",
        "customer_phone": "+7 900 802 33 33",
        "order_date": "invalid_date"
    }

    response = client.post("/forms/get_form/", json=data)

    assert response.status_code == 200
    assert response.json() == {
        "customer_email": "email",
        "customer_phone": "phone",
        "order_date": "text"
    }
