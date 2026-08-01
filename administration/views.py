import os
import shutil
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import FileResponse, Http404
from accounts.models import User
from accounts.decorators import library_helper_required, head_librarian_required
from audit.utils import log_action
from django.contrib import messages

from notifications.services import (
    send_due_reminders,
    send_overdue_reminders,
)

from audit.utils import log_action


@login_required
@library_helper_required
def home(request):

    return render(
        request,
        "administration/home.html",
    )


@login_required
@library_helper_required
def backup_database(request):

    backup_dir = settings.BACKUP_DIR

    if request.method == "POST":

        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        filename = f"library_backup_{timestamp}.sqlite3"

        source = settings.BASE_DIR / "db.sqlite3"

        destination = backup_dir / filename

        shutil.copy2(source, destination)

        log_action(
            request.user,
            "Database Backup Created",
            filename,
        )

        messages.success(
            request,
            "Database backup created successfully.",
        )

        return redirect("backup_database")

    backups = []

    for file in sorted(
        os.listdir(backup_dir),
        reverse=True,
    ):

        path = backup_dir / file

        backups.append(
            {
                "name": file,
                "size": round(
                    os.path.getsize(path) / (1024 * 1024),
                    2,
                ),
                "created": datetime.fromtimestamp(
                    os.path.getctime(path)
                ),
            }
        )

    db_size = round(
        os.path.getsize(settings.BASE_DIR / "db.sqlite3")
        / (1024 * 1024),
        2,
    )

    latest_backup = backups[0] if backups else None

    return render(
        request,
        "administration/backup.html",
        {
            "db_size": db_size,
            "backups": backups,
            "latest_backup": latest_backup,
        },
    )

@login_required
@library_helper_required
def download_backup(request, filename):

    filepath = settings.BACKUP_DIR / filename

    if not filepath.exists():
        raise Http404("Backup file not found.")

    log_action(
        request.user,
        "Database Backup Downloaded",
        filename,
    )

    return FileResponse(
        open(filepath, "rb"),
        as_attachment=True,
        filename=filename,
    )

@login_required
@library_helper_required
def delete_backup(request, filename):

    filepath = settings.BACKUP_DIR / filename

    if not filepath.exists():

        raise Http404("Backup file not found.")

    if request.method == "POST":

        os.remove(filepath)

        log_action(
            request.user,
            "Database Backup Deleted",
            filename,
        )

        messages.success(
            request,
            "Backup deleted successfully.",
        )

        return redirect("backup_database")

    return render(
        request,
        "administration/delete_backup.html",
        {
            "filename": filename,
        },
    )


@login_required
@library_helper_required
def send_due_reminders_view(request):

    sent = send_due_reminders()

    log_action(
        request.user,
        "Due Reminder Emails",
        f"Sent {sent} reminder emails.",
    )

    messages.success(
        request,
        f"{sent} due reminder emails generated successfully.",
    )

    return redirect("administration_home")


@login_required
@library_helper_required
def send_overdue_reminders_view(request):

    sent = send_overdue_reminders()

    log_action(
        request.user,
        "Overdue Reminder Emails",
        f"Sent {sent} overdue reminder emails.",
    )

    messages.success(
        request,
        f"{sent} overdue reminder emails generated successfully.",
    )

    return redirect("administration_home")

@login_required
@head_librarian_required
def manage_users(request):

    users = User.objects.order_by("username")

    if request.method == "POST":

        for user in users:

            if user == request.user:
                continue

            if user.role == "head_librarian" and request.POST.get(f"role_{user.id}") != "head_librarian":

                messages.error(
                    request,
                    f"{user.username} is a Head Librarian and cannot be demoted from here."
                )

                continue

            new_role = request.POST.get(f"role_{user.id}")

            if new_role and new_role != user.role:

                user.role = new_role
                user.save()

        messages.success(
            request,
            "User roles updated successfully."
        )

        return redirect("manage_users")

    return render(
        request,
        "administration/manage_users.html",
        {
            "users": users,
            "roles": User.ROLE_CHOICES,
        },
    )