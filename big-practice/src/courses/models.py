from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DurationField()
    description = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.name
