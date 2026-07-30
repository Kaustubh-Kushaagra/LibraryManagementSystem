from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def build_due_reminder(transaction):

    subject = "MVTC Library - Book Due Reminder"

    context = {
        "transaction": transaction,
        "member": transaction.member,
        "book": transaction.book,
    }

    text_body = render_to_string(
        "emails/due_reminder.txt",
        context,
    )

    html_body = render_to_string(
        "emails/due_reminder.html",
        context,
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        to=[transaction.member.email],
    )

    email.attach_alternative(
        html_body,
        "text/html",
    )

    return email


def build_overdue_reminder(transaction):

    subject = "MVTC Library - Book Overdue"

    context = {
        "transaction": transaction,
        "member": transaction.member,
        "book": transaction.book,
    }

    text_body = render_to_string(
        "emails/overdue_reminder.txt",
        context,
    )

    html_body = render_to_string(
        "emails/overdue_reminder.html",
        context,
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        to=[transaction.member.email],
    )

    email.attach_alternative(
        html_body,
        "text/html",
    )

    return email