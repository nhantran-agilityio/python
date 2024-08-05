from django.db import models


class Report(models.Model):
    point = models.PositiveIntegerField()
    description = models.CharField(max_length=150, null=True)

    # student = models.OneToOneField('Student', on_delete=models.CASCADE,
    #                                related_name='report')
    # course = models.OneToOneField('Course', on_delete=models.CASCADE,
    #                               related_name='report')

    def __str__(self):
        return self.point
