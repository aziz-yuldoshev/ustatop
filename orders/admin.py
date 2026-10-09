from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "service",
        "get_master",
        "agreed_price",
        "status",
        "scheduled_at",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
        "scheduled_at",
    )

    search_fields = (
        "customer__username",
        "customer__first_name",
        "customer__last_name",
        "service__title",
        "service__master__user__username",
        "phone",
        "address",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "completed_at",
    )

    date_hierarchy = "created_at"

    def get_master(self, obj):
        return obj.service.master

    get_master.short_description = "Usta"