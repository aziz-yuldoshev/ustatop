from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.shortcuts import render, redirect

from accounts.models import User
from orders.models import Order
from reviews.models import Review
from services.models import (
    Service,
    ServiceCategory,
    MasterProfile,
)


@login_required
def dashboard_home(request):

    user = request.user

    # ADMIN
    if user.is_staff or user.is_superuser:
        return admin_dashboard(request)

    # MASTER
    if user.role == "master":
        return master_dashboard(request)

    # CUSTOMER
    return customer_dashboard(request)


@login_required
def admin_dashboard(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect("dashboard")

    # USERS
    total_users = User.objects.count()

    total_customers = User.objects.filter(
        role="customer"
    ).count()

    total_masters = User.objects.filter(
        role="master"
    ).count()

    verified_masters = MasterProfile.objects.filter(
        is_verified=True
    ).count()

    # SERVICES
    total_services = Service.objects.count()

    active_services = Service.objects.filter(
        is_active=True
    ).count()

    total_categories = ServiceCategory.objects.count()

    # ORDERS
    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(
        status="pending"
    ).count()

    active_orders = Order.objects.filter(
        status__in=[
            "accepted",
            "in_progress",
        ]
    ).count()

    completed_orders = Order.objects.filter(
        status="completed"
    ).count()

    rejected_orders = Order.objects.filter(
        status="rejected"
    ).count()

    # MONEY
    total_earnings = (
        Order.objects
        .filter(status="completed")
        .aggregate(
            total=Sum("agreed_price")
        )["total"]
        or 0
    )

    # REVIEWS
    total_reviews = Review.objects.count()

    average_rating = (
        Review.objects
        .filter(is_visible=True)
        .aggregate(
            average=Avg("rating")
        )["average"]
        or 0
    )

    # RECENT ORDERS
    recent_orders = (
        Order.objects
        .select_related(
            "customer",
            "service",
            "service__master__user",
        )
        .order_by("-created_at")[:8]
    )

    # RECENT MASTERS
    recent_masters = (
        MasterProfile.objects
        .select_related("user")
        .order_by("-created_at")[:6]
    )

    context = {
        "total_users": total_users,
        "total_customers": total_customers,
        "total_masters": total_masters,
        "verified_masters": verified_masters,

        "total_services": total_services,
        "active_services": active_services,
        "total_categories": total_categories,

        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "active_orders": active_orders,
        "completed_orders": completed_orders,
        "rejected_orders": rejected_orders,

        "total_earnings": total_earnings,

        "total_reviews": total_reviews,
        "average_rating": average_rating,

        "recent_orders": recent_orders,
        "recent_masters": recent_masters,
    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context,
    )


@login_required
def customer_dashboard(request):

    orders = (
        Order.objects
        .filter(customer=request.user)
        .select_related(
            "service",
            "service__master__user",
            "service__category",
        )
    )

    total_orders = orders.count()

    pending_orders = orders.filter(
        status="pending"
    ).count()

    active_orders = orders.filter(
        status__in=[
            "accepted",
            "in_progress",
        ]
    ).count()

    completed_orders = orders.filter(
        status="completed"
    ).count()

    recent_orders = orders[:6]

    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "active_orders": active_orders,
        "completed_orders": completed_orders,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "dashboard/customer_dashboard.html",
        context,
    )


@login_required
def master_dashboard(request):

    if request.user.role != "master":
        return customer_dashboard(request)

    master = request.user.master_profile

    services = Service.objects.filter(
        master=master
    )

    orders = (
        Order.objects
        .filter(service__master=master)
        .select_related(
            "customer",
            "service",
            "service__category",
        )
    )

    total_services = services.count()

    total_orders = orders.count()

    pending_orders = orders.filter(
        status="pending"
    ).count()

    active_orders = orders.filter(
        status__in=[
            "accepted",
            "in_progress",
        ]
    ).count()

    completed_orders = orders.filter(
        status="completed"
    ).count()

    total_earnings = (
        orders
        .filter(status="completed")
        .aggregate(
            total=Sum("agreed_price")
        )["total"]
        or 0
    )

    recent_orders = orders[:8]

    context = {
        "master": master,
        "services": services,
        "total_services": total_services,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "active_orders": active_orders,
        "completed_orders": completed_orders,
        "total_earnings": total_earnings,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "dashboard/master_dashboard.html",
        context,
    )