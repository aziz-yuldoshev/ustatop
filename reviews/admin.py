from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "service",
        "rating",
        "is_visible",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_visible",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__first_name",
        "customer__last_name",
        "service__title",
        "comment",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )