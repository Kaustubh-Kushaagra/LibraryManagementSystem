from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
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




@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    )

    paginator = Paginator(
        notifications,
        20,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "notifications/list.html",
        {
            "page_obj": page_obj,
        },
    )

@login_required
def mark_all_read(request):

    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(is_read=True)

    return redirect("notification_list")