from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    )

    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(
        is_read=True
    )

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
        },
    )


@login_required
def mark_notification_read(
    request,
    notification_id,
):

    notification = Notification.objects.get(
        id=notification_id,
        user=request.user,
    )

    notification.is_read = True
    notification.save(
        update_fields=["is_read"]
    )

    if notification.link:
        return redirect(notification.link)

    return redirect("notifications")