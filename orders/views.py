from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from notifications.models import Notification
from services.models import Service

from .forms import OrderCreateForm
from .models import Order


@login_required
def create_order(request, service_id):

    service = get_object_or_404(
        Service.objects.select_related(
            "master__user",
            "category",
        ),
        pk=service_id,
        is_active=True,
    )

    if request.method == "POST":

        form = OrderCreateForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.customer = request.user
            order.service = service
            order.agreed_price = service.price

            order.save()

            # 🔔 USTAGA YANGI BUYURTMA NOTIFICATIONI
            Notification.objects.create(
                user=service.master.user,
                title="Yangi buyurtma 📦",
                message=(
                    f"{request.user.get_full_name() or request.user.username} "
                    f"“{service.title}” xizmatiga buyurtma berdi."
                ),
                notification_type="order",
                link=reverse(
                    "order_detail",
                    kwargs={
                        "order_id": order.id
                    }
                ),
            )

            messages.success(
                request,
                "Buyurtmangiz muvaffaqiyatli yuborildi!",
            )

            return redirect(
                "order_detail",
                order_id=order.id,
            )

    else:

        form = OrderCreateForm(
            initial={
                "phone": request.user.phone,
                "address": request.user.address,
            }
        )

    return render(
        request,
        "orders/create_order.html",
        {
            "service": service,
            "form": form,
        },
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            "customer",
            "service",
            "service__master__user",
            "service__category",
        ),
        pk=order_id,
    )

    if (
        request.user != order.customer
        and request.user != order.service.master.user
    ):
        messages.error(
            request,
            "Bu buyurtmani ko‘rish huquqingiz yo‘q.",
        )

        return redirect("home")

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order
        },
    )


@login_required
def my_orders(request):

    # 👤 MIJOZNING BUYURTMALARI
    orders = (
        Order.objects
        .filter(
            customer=request.user
        )
        .select_related(
            "customer",
            "service",
            "service__master__user",
            "service__category",
        )
    )

    # 🔧 USTAGA KELGAN BUYURTMALAR
    master_orders = (
        Order.objects
        .filter(
            service__master__user=request.user
        )
        .select_related(
            "customer",
            "service",
            "service__master__user",
            "service__category",
        )
    )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders,
            "master_orders": master_orders,
        },
    )


@login_required
def accept_order(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            "customer",
            "service__master__user",
        ),
        pk=order_id,
    )

    if request.user != order.service.master.user:

        messages.error(
            request,
            "Bu buyurtmani boshqarish huquqingiz yo‘q.",
        )

        return redirect("home")

    if order.status != "pending":

        messages.warning(
            request,
            "Bu buyurtma hozir qabul qilinishi mumkin emas.",
        )

        return redirect(
            "order_detail",
            order_id=order.id,
        )

    order.status = "accepted"

    order.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    # 🔔 MIJOZGA NOTIFICATION
    Notification.objects.create(
        user=order.customer,
        title="Buyurtma qabul qilindi ✅",
        message=(
            f"Usta “{order.service.title}” "
            f"buyurtmangizni qabul qildi."
        ),
        notification_type="order",
        link=reverse(
            "order_detail",
            kwargs={
                "order_id": order.id
            }
        ),
    )

    messages.success(
        request,
        "Buyurtma qabul qilindi!",
    )

    return redirect(
        "order_detail",
        order_id=order.id,
    )


@login_required
def reject_order(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            "customer",
            "service__master__user",
        ),
        pk=order_id,
    )

    if request.user != order.service.master.user:

        messages.error(
            request,
            "Bu buyurtmani boshqarish huquqingiz yo‘q.",
        )

        return redirect("home")

    if order.status != "pending":

        messages.warning(
            request,
            "Bu buyurtma rad etilishi mumkin emas.",
        )

        return redirect(
            "order_detail",
            order_id=order.id,
        )

    order.status = "rejected"

    order.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    # 🔔 MIJOZGA NOTIFICATION
    Notification.objects.create(
        user=order.customer,
        title="Buyurtma rad etildi ❌",
        message=(
            f"Usta “{order.service.title}” "
            f"buyurtmangizni rad etdi."
        ),
        notification_type="order",
        link=reverse(
            "order_detail",
            kwargs={
                "order_id": order.id
            }
        ),
    )

    messages.success(
        request,
        "Buyurtma rad etildi.",
    )

    return redirect(
        "order_detail",
        order_id=order.id,
    )


@login_required
def start_order(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            "customer",
            "service__master__user",
        ),
        pk=order_id,
    )

    if request.user != order.service.master.user:

        messages.error(
            request,
            "Bu buyurtmani boshqarish huquqingiz yo‘q.",
        )

        return redirect("home")

    if order.status != "accepted":

        messages.warning(
            request,
            "Faqat qabul qilingan buyurtmani boshlash mumkin.",
        )

        return redirect(
            "order_detail",
            order_id=order.id,
        )

    order.status = "in_progress"

    order.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    # 🔔 MIJOZGA NOTIFICATION
    Notification.objects.create(
        user=order.customer,
        title="Xizmat boshlandi 🔨",
        message=(
            f"“{order.service.title}” "
            f"xizmati bo‘yicha buyurtmangiz boshlandi."
        ),
        notification_type="order",
        link=reverse(
            "order_detail",
            kwargs={
                "order_id": order.id
            }
        ),
    )

    messages.success(
        request,
        "Buyurtma jarayonga olindi!",
    )

    return redirect(
        "order_detail",
        order_id=order.id,
    )


@login_required
def complete_order(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            "customer",
            "service__master__user",
        ),
        pk=order_id,
    )

    if request.user != order.service.master.user:

        messages.error(
            request,
            "Bu buyurtmani boshqarish huquqingiz yo‘q.",
        )

        return redirect("home")

    if order.status != "in_progress":

        messages.warning(
            request,
            "Faqat jarayondagi buyurtmani tugatish mumkin.",
        )

        return redirect(
            "order_detail",
            order_id=order.id,
        )

    order.status = "completed"
    order.completed_at = timezone.now()

    order.save(
        update_fields=[
            "status",
            "completed_at",
            "updated_at",
        ]
    )

    # 🔧 USTA STATISTIKASINI YANGILASH
    master = order.service.master

    master.completed_orders += 1

    master.save(
        update_fields=[
            "completed_orders",
        ]
    )

    # 🔔 MIJOZGA NOTIFICATION
    Notification.objects.create(
        user=order.customer,
        title="Buyurtma tugallandi 🎉",
        message=(
            f"“{order.service.title}” "
            f"xizmati bo‘yicha buyurtmangiz "
            f"muvaffaqiyatli tugallandi."
        ),
        notification_type="order",
        link=reverse(
            "order_detail",
            kwargs={
                "order_id": order.id
            }
        ),
    )

    messages.success(
        request,
        "Buyurtma muvaffaqiyatli tugatildi! 🎉",
    )

    return redirect(
        "order_detail",
        order_id=order.id,
    )