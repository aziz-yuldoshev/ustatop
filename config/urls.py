from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from services import views as service_views


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Orders
    path("orders/", include("orders.urls")),

    # Reviews
    path("reviews/", include("reviews.urls")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # Favorites
    path("favorites/", include("favorites.urls")),

    # Notifications
    path("notifications/", include("notifications.urls")),

    # Service detail
    path(
        "service/<int:service_id>/",
        service_views.service_detail,
        name="service_detail",
    ),

    # Master detail
    path(
        "master/<int:master_id>/",
        service_views.master_detail,
        name="master_detail",
    ),

    # Home
    path(
        "",
        service_views.home,
        name="home",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )