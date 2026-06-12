import os
from pathlib import Path

from django.apps import AppConfig
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_PK_FIELD = (
    "django_mongodb_backend.fields.ObjectIdAutoField"
    if os.environ.get("MONGO_URI", "").strip()
    else "django.db.models.BigAutoField"
)


class EventsConfig(AppConfig):
    default_auto_field = _PK_FIELD
    name = "events"
