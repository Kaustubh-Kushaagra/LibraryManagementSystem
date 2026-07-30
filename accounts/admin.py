from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "employee_id",
        "first_name",
        "last_name",
        "department",
        "designation",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "department",
        "is_active",
    )

    search_fields = (
        "username",
        "employee_id",
        "first_name",
        "last_name",
        "email",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Company Information",
            {
                "fields": (
                    "employee_id",
                    "department",
                    "designation",
                    "phone",
                    "address",
                    "profile_picture",
                    "role",
                )
            },
        ),
    )