from notifications.models import Notification


def notifications_context(request):

    if not request.user.is_authenticated:
        return {
            "unread_notifications_count": 0,
            "recent_notifications": [],
        }

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return {
        "unread_notifications_count": notifications.filter(
            is_read=False
        ).count(),

        "recent_notifications": notifications[:5],
    }