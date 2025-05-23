import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class AbstractBaseModel(TimeStampedModel, models.Model):
    """
    Base abstract model that includes "id"
    and includes "created", "modified" timestamp fields.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )

    class Meta:
        abstract = True


class BaseModelQuerySet(models.QuerySet):
    user_relation_field = 'user'

    def for_user(self, user):
        if user.is_admin:
            # If the user is an admin, return all objects
            # without filtering by user
            return self
        filter_kwargs = {self.user_relation_field: user}
        return self.filter(**filter_kwargs)


class LeaveApplicationQuerySet(BaseModelQuerySet):
    user_relation_field = 'employee'
