from datetime import timedelta

from django.utils import timezone

from .utils import (
    build_due_reminder,
    build_overdue_reminder,
)

from transactions.models import Transaction


def get_due_soon_transactions():

    target_date = timezone.now().date() + timedelta(days=2)

    return Transaction.objects.filter(
        status="Issued",
        due_date=target_date,
        member__email__isnull=False,
    ).exclude(
        member__email=""
    )


def get_overdue_transactions():

    today = timezone.now().date()

    return Transaction.objects.filter(
        status="Issued",
        due_date__lt=today,
        member__email__isnull=False,
    ).exclude(
        member__email=""
    )


def send_due_reminders():

    count = 0

    for transaction in get_due_soon_transactions():

        email = build_due_reminder(transaction)

        email.send()

        count += 1

    return count


def send_overdue_reminders():

    count = 0

    for transaction in get_overdue_transactions():

        email = build_overdue_reminder(transaction)

        email.send()

        count += 1

    return count