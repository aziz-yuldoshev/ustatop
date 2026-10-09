from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order
from services.models import Service

from .forms import ReviewForm
from .models import Review


@login_required
def create_review(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            "service",
            "service__master__user",
        ),
        pk=order_id,
        customer=request.user,
        status="completed",
    )

    if hasattr(order, "review"):
        messages.info(
            request,
            "Bu buyurtma uchun allaqachon sharh qoldirgansiz.",
        )
        return redirect("order_detail", order_id=order.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.service = order.service
            review.order = order
            review.save()

            update_master_rating(order.service.master)

            messages.success(
                request,
                "Rahmat! Sharhingiz muvaffaqiyatli yuborildi.",
            )

            return redirect(
                "order_detail",
                order_id=order.id,
            )

    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/create_review.html",
        {
            "order": order,
            "form": form,
        },
    )


def service_reviews(request, service_id):

    service = get_object_or_404(
        Service.objects.select_related(
            "master__user",
            "category",
        ),
        pk=service_id,
        is_active=True,
    )

    reviews = (
        Review.objects
        .filter(
            service=service,
            is_visible=True,
        )
        .select_related("customer")
    )

    rating_stats = reviews.aggregate(
        average=Avg("rating")
    )

    return render(
        request,
        "reviews/service_reviews.html",
        {
            "service": service,
            "reviews": reviews,
            "average_rating": rating_stats["average"] or 0,
        },
    )


def update_master_rating(master):

    average = (
        Review.objects
        .filter(
            service__master=master,
            is_visible=True,
        )
        .aggregate(
            average=Avg("rating")
        )["average"]
    )

    master.rating = round(average or 0, 2)
    master.save(update_fields=["rating"])