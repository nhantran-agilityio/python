from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
