from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'

    def ready(self):
        import accounts.signals


# class AccountsConfig(AppConfig):
#     name = 'accounts'

#     def ready(self):
#         import accounts.signals
