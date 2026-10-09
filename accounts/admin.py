from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "role",
        "phone",
        "is_verified",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "phone",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "USTATOP ma'lumotlari",
            {
                "fields": (
                    "role",
                    "phone",
                    "address",
                    "avatar",
                    "is_verified",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "USTATOP ma'lumotlari",
            {
                "fields": (
                    "role",
                    "phone",
                    "address",
                    "avatar",
                    "is_verified",
                )
            },
        ),
    )