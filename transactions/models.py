from django.conf import settings
from django.db import models

from books.models import LibraryItem


class Transaction(models.Model):

    PENDING_PICKUP = "Pending Pickup"
    ISSUED = "Issued"
    RETURNED = "Returned"

    STATUS_CHOICES = [
        (PENDING_PICKUP, "Pending Pickup"),
        (ISSUED, "Issued"),
        (RETURNED, "Returned"),
    ]

    RETURN_NONE = "None"
    RETURN_REQUESTED = "Requested"
    RETURN_APPROVED = "Approved"

    RETURN_STATUS_CHOICES = [
        (RETURN_NONE, "None"),
        (RETURN_REQUESTED, "Requested"),
        (RETURN_APPROVED, "Approved"),
    ]

    book = models.ForeignKey(
        LibraryItem,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    issued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    returned_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ISSUED,
    )

    remarks = models.TextField(
        blank=True,
    )

    return_status = models.CharField(
        max_length=20,
        choices=RETURN_STATUS_CHOICES,
        default=RETURN_NONE,
    )

    return_requested_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    return_pickup_date = models.DateField(
        blank=True,
        null=True,
    )

    return_pickup_time = models.TimeField(
        blank=True,
        null=True,
    )

    librarian_return_message = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self):
        return f"{self.book.title} → {self.member.username}"