from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from services.models import Service

from .models import Favorite


@login_required
def toggle_favorite(request, service_id):

    if request.method != "POST":
        return redirect("service_detail", service_id=service_id)

    service = get_object_or_404(
        Service,
        id=service_id,
        is_active=True,
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        service=service,
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            service=service,
        )

    return redirect(
        request.POST.get(
            "next",
            request.META.get("HTTP_REFERER", "/")
        )
    )


@login_required
def favorite_list(request):

    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related(
            "service",
            "service__master__user",
            "service__category",
        )
    )

    return render(
        request,
        "favorites/favorite_list.html",
        {
            "favorites": favorites,
        },
    )