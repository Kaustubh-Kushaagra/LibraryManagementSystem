from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.notification_list,
        name="notification_list",
    ),

    path(
        "read/<int:pk>/",
        views.read_notification,
        name="read_notification",
    ),

    path(
        "mark-all-read/",
        views.mark_all_read,
        name="mark_all_read",
    ),

]