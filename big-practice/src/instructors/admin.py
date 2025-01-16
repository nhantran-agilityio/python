from django.contrib import admin
from .models import Instructor


class InstructorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


# Register your models here.
admin.site.register(Instructor, InstructorsAdmin)
