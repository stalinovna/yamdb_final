from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    App Config for Users application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"
