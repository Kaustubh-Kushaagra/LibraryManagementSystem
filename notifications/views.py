from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Notification


@login_required
def read_notification(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user,
    )

    notification.is_read = True
    notification.save()

    if notification.link:
        return redirect(notification.link)

    return redirect("dashboard")