from django.contrib import admin

from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "service",
        "created_at",
    )

    search_fields = (
        "user__username",
        "service__title",
    )

    readonly_fields = (
        "created_at",
    )