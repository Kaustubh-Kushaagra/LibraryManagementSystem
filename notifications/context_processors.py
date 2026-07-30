from .models import Notification


def notification_context(request):

    if not request.user.is_authenticated:

        return {
            "notifications": [],
            "unread_notification_count": 0,
        }

    notifications = (
        Notification.objects.filter(
            user=request.user,
        )
        .order_by("-created_at")[:5]
    )

    unread_count = (
        Notification.objects.filter(
            user=request.user,
            is_read=False,
        )
        .count()
    )

    return {
        "notifications": notifications,
        "unread_notification_count": unread_count,
    }