from django.db import models

from src.core.utils import get_upload_path


class ReceiptTemplate(models.Model):
    title = models.CharField()
    file = models.FileField(upload_to=get_upload_path)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}" if not self.is_selected else f"{self.title} (за замовчуванням)"
