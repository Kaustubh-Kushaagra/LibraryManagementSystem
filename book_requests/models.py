from django.db import models
from django.conf import settings
from books.models import LibraryItem
from transactions.models import Transaction


class BookRequest(models.Model):

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    READY = "Ready for Pickup"
    COLLECTED = "Collected"
    CANCELLED = "Cancelled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (READY, "Ready for Pickup"),
        (COLLECTED, "Collected"),
        (CANCELLED, "Cancelled"),
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="book_requests",
    )

    book = models.ForeignKey(
        LibraryItem,
        on_delete=models.CASCADE,
        related_name="requests",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    requested_at = models.DateTimeField(auto_now_add=True)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_requests",
    )

    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_requests",
    )

    rejected_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    rejection_reason = models.TextField(
        blank=True,
    )

    pickup_date = models.DateField(
        null=True,
        blank=True,
    )

    pickup_time = models.TimeField(
        null=True,
        blank=True,
    )

    librarian_message = models.TextField(
        blank=True,
    )

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.member} → {self.book.title}"