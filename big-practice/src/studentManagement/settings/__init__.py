"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
To change settings file:
`DJANGO_ENV=prod python manage.py runserver`
"""

from os import environ

from split_settings.tools import include

# Managing environment via DJANGO_ENV variable:
environ.setdefault("DJANGO_ENV", "dev")
ENV = environ["DJANGO_ENV"]

base_settings = [
    # Select the right env:
    'base.py',
    f"{ENV}.py",
]

# Include settings:
include(*base_settings)
