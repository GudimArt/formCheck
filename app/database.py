import os

from tinydb import TinyDB

project_root = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(project_root, '..', 'template_forms.json')
db_path = os.path.abspath(DB_PATH)
db = TinyDB(DB_PATH)


def get_db() -> TinyDB:
    yield db
