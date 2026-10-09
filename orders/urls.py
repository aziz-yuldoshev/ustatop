from django.urls import path

from . import views


urlpatterns = [

    path(
        "create/<int:service_id>/",
        views.create_order,
        name="create_order",
    ),

    path(
        "my/",
        views.my_orders,
        name="my_orders",
    ),

    path(
        "<int:order_id>/",
        views.order_detail,
        name="order_detail",
    ),

    path(
        "<int:order_id>/accept/",
        views.accept_order,
        name="accept_order",
    ),

    path(
        "<int:order_id>/reject/",
        views.reject_order,
        name="reject_order",
    ),

    path(
        "<int:order_id>/start/",
        views.start_order,
        name="start_order",
    ),

    path(
        "<int:order_id>/complete/",
        views.complete_order,
        name="complete_order",
    ),
]