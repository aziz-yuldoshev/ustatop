from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.notification_list,
        name="notifications",
    ),

    path(
        "<int:notification_id>/read/",
        views.mark_notification_read,
        name="notification_read",
    ),
]