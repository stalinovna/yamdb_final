from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    Creating ModelAdmin for User model.
    """

    fields = [
        ("username", "email"),
        ("first_name", "last_name"),
        ("is_active", "is_staff", "is_superuser"),
        "role",
        "bio",
        "last_login",
        "date_joined",
    ]
    readonly_fields = ("last_login", "date_joined")
    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "role",
        "last_login"
    )
    search_fields = ("username",)
    list_filter = ("role",)
    empty_value_display = "-пусто-"
    exclude = ("password", "user_permissions", "date_joined", "groups")


admin.site.register(User, UserAdmin)
