from django.db import models
from accounts.models import User
from core.models import AbstractBaseModel, BaseModelManager, BaseModelQuerySet


class Notification(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    recall_id = models.UUIDField(null=True, blank=True)
    objects = BaseModelManager.from_queryset(BaseModelQuerySet)()

    def __str__(self):
        return f"Notification for {self.user.username}"
