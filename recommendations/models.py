from django.conf import settings
from django.db import models


class BookRecommendation(models.Model):

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="book_recommendations",
    )

    title = models.CharField(max_length=255)

    author = models.CharField(max_length=255)

    publisher = models.CharField(
        max_length=255,
        blank=True,
    )

    isbn = models.CharField(
        max_length=50,
        blank=True,
    )

    edition = models.CharField(
        max_length=100,
        blank=True,
    )

    category = models.CharField(
        max_length=100,
        blank=True,
    )

    language = models.CharField(
        max_length=100,
        blank=True,
    )

    approximate_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    reason = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    librarian_notes = models.TextField(
        blank=True,
    )

    requested_at = models.DateTimeField(
        auto_now_add=True,
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title