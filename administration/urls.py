from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="administration_home",
    ),

    path(
        "backup/",
        views.backup_database,
        name="backup_database",
    ),

    path(
        "backup/download/<str:filename>/",
        views.download_backup,
        name="download_backup",
    ),

    path(
        "backup/delete/<str:filename>/",
        views.delete_backup,
        name="delete_backup",
    ),

    path(
        "send-due-reminders/",
        views.send_due_reminders_view,
        name="send_due_reminders",
    ),

    path(
        "send-overdue-reminders/",
        views.send_overdue_reminders_view,
        name="send_overdue_reminders",
    ),

]