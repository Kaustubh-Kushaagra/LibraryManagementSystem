from django.db import models
from django.core.validators import MinValueValidator
from donors.models import Donor

# ===========================
# CATEGORY
# ===========================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# ===========================
# AUTHOR
# ===========================

class Author(models.Model):
    name = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ===========================
# PUBLISHER
# ===========================

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name




# ===========================
# LIBRARY ITEM
# ===========================

class LibraryItem(models.Model):

    PURCHASE = "Purchase"
    DONATION = "Donation"
    GOVERNMENT = "Government"
    OTHER = "Other"

    ACQUISITION_CHOICES = [
        (PURCHASE, "Purchase"),
        (DONATION, "Donation"),
        (GOVERNMENT, "Government"),
        (OTHER, "Other"),
    ]

    AVAILABLE = "Available"
    ISSUED = "Issued"
    MAINTENANCE = "Maintenance"
    ARCHIVED = "Archived"

    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (ISSUED, "Issued"),
        (MAINTENANCE, "Maintenance"),
        (ARCHIVED, "Archived"),
    ]

    accession_number = models.CharField(
        max_length=50,
        unique=True
    )

    serial_number = models.PositiveIntegerField(
    unique=True,
    null=True,
    blank=True
    )

    date_added = models.DateField(
        null=True,
        blank=True
    )

    source = models.CharField(
        max_length=255,
        blank=True,
        help_text="Purchase or Donated by..."
    )

    title = models.CharField(max_length=300)

    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books"
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.PROTECT,
        related_name="books"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="books"
    )

    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    pages = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    volume_qty = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    acquisition_type = models.CharField(
        max_length=20,
        choices=ACQUISITION_CHOICES,
        default=PURCHASE
    )

    donor = models.ForeignKey(
        Donor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donated_books"
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: Rack A-01"
    )

    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "accession_number"]

    def __str__(self):
        return f"{self.accession_number} - {self.title}"