from django.urls import path

from . import views


urlpatterns = [
    path(
        "create/<int:order_id>/",
        views.create_review,
        name="create_review",
    ),

    path(
        "service/<int:service_id>/",
        views.service_reviews,
        name="service_reviews",
    ),
]