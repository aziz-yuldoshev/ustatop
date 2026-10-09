from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Service, ServiceCategory, MasterProfile


def home(request):

    categories = ServiceCategory.objects.filter(
        is_active=True
    ).order_by("name")

    search = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "").strip()
    area = request.GET.get("area", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    services = (
        Service.objects
        .filter(is_active=True)
        .select_related(
            "master__user",
            "category",
        )
        .order_by("-created_at")
    )

    if search:
        services = services.filter(
            Q(title__icontains=search)
            |
            Q(description__icontains=search)
            |
            Q(category__name__icontains=search)
            |
            Q(master__profession__icontains=search)
            |
            Q(master__user__first_name__icontains=search)
            |
            Q(master__user__last_name__icontains=search)
        )

    if category_id:
        services = services.filter(
            category_id=category_id
        )

    if area:
        services = services.filter(
            master__service_area__icontains=area
        )

    if min_price:
        try:
            services = services.filter(
                price__gte=float(min_price)
            )
        except (ValueError, TypeError):
            pass

    if max_price:
        try:
            services = services.filter(
                price__lte=float(max_price)
            )
        except (ValueError, TypeError):
            pass

    services = services[:20]

    masters = (
        MasterProfile.objects
        .filter(
            is_available=True,
            is_verified=True,
        )
        .select_related("user")
        .order_by(
            "-rating",
            "-completed_orders"
        )
    )

    context = {
        "categories": categories,
        "services": services,
        "masters": masters,
        "search": search,
        "selected_category": category_id,
        "area": area,
        "min_price": min_price,
        "max_price": max_price,
    }

    return render(
        request,
        "services/home.html",
        context
    )


def service_detail(request, service_id):

    service = get_object_or_404(
        Service.objects.select_related(
            "master__user",
            "category",
        ),
        pk=service_id,
        is_active=True,
    )

    reviews = (
        service.reviews
        .filter(is_visible=True)
        .select_related("customer")
        .order_by("-created_at")[:10]
    )

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = service.favorited_by.filter(
            user=request.user
        ).exists()

    context = {
        "service": service,
        "reviews": reviews,
        "is_favorite": is_favorite,
    }

    return render(
        request,
        "services/service_detail.html",
        context
    )

def master_detail(request, master_id):
    master = get_object_or_404(
        MasterProfile.objects.select_related("user"),
        id=master_id,
    )

    services = (
        Service.objects
        .filter(
            master=master,
            is_active=True
        )
        .select_related("category")
        .order_by("-created_at")
    )

    return render(
        request,
        "services/master_detail.html",
        {
            "master": master,
            "services": services,
        },
    )