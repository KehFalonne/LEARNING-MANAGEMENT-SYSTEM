
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "University Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "profile_picture",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "University Information",
            {
                "fields": (
                    "email",
                    "role",
                    "phone",
                    "profile_picture",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )