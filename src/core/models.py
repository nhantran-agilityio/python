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


class BaseModelManager(models.Manager):
    def visible_to(self, user):
        return self.get_queryset().visible_to(user)


class BaseModelQuerySet(models.QuerySet):
    user_relation_field = 'user'

    def visible_to(self, user):
        if user.is_authenticated is False:
            # Handle unauthenticated users (e.g., return an empty queryset)
            return self.none()

        if user.is_admin:
            # If the user is an admin, return all objects
            # without filtering by user
            return self
        filter_kwargs = {self.user_relation_field: user}
        return self.filter(**filter_kwargs)
