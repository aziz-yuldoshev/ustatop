from django.contrib import admin

from .models import (
    MasterProfile,
    Service,
    ServiceCategory,
)


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "profession",
        "service_area",
        "experience_years",
        "hourly_rate",
        "rating",
        "completed_orders",
        "is_available",
        "is_verified",
    )

    list_filter = (
        "is_available",
        "is_verified",
        "profession",
        "service_area",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__phone",
        "profession",
        "service_area",
    )

    list_editable = (
        "is_available",
        "is_verified",
    )

    readonly_fields = (
        "rating",
        "completed_orders",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "👤 Usta ma'lumotlari",
            {
                "fields": (
                    "user",
                    "profession",
                    "bio",
                    "experience_years",
                    "service_area",
                )
            },
        ),
        (
            "💰 Xizmat va holat",
            {
                "fields": (
                    "hourly_rate",
                    "is_available",
                    "is_verified",
                )
            },
        ),
        (
            "⭐ Statistika",
            {
                "fields": (
                    "rating",
                    "completed_orders",
                )
            },
        ),
        (
            "📅 Tizim ma'lumotlari",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "icon",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "is_active",
    )

    prepopulated_fields = {}

    fieldsets = (
        (
            "📂 Kategoriya ma'lumotlari",
            {
                "fields": (
                    "name",
                    "description",
                    "icon",
                    "is_active",
                )
            },
        ),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "master",
        "category",
        "price",
        "price_type",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "price_type",
        "category",
    )

    search_fields = (
        "title",
        "description",
        "master__user__username",
        "master__user__first_name",
        "master__user__last_name",
        "master__profession",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "master",
        "category",
    )

    fieldsets = (
        (
            "🛠️ Xizmat ma'lumotlari",
            {
                "fields": (
                    "title",
                    "description",
                    "master",
                    "category",
                )
            },
        ),
        (
            "💰 Narx",
            {
                "fields": (
                    "price",
                    "price_type",
                )
            },
        ),
        (
            "🖼️ Rasm va holat",
            {
                "fields": (
                    "image",
                    "is_active",
                )
            },
        ),
        (
            "📅 Tizim ma'lumotlari",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )