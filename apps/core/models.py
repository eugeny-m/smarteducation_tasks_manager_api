import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models.
    Provides UUID for external API identification and timestamps.
    """
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
        help_text="UUID for external API identification"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
