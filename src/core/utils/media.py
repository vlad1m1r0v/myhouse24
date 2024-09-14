from uuid import uuid4
from django.db.models import Model


def get_upload_path(model: Model, filename: str) -> str:
    extension = filename.split('.')[-1]
    uuid = uuid4()
    return f'{model._meta.model_name}/{uuid}.{extension}'