from django.db import models


class Donor(models.Model):

    INDIVIDUAL = "Individual"
    COMPANY = "Company"
    INSTITUTION = "Institution"
    GOVERNMENT = "Government"

    DONOR_TYPES = [
        (INDIVIDUAL, "Individual"),
        (COMPANY, "Company"),
        (INSTITUTION, "Institution"),
        (GOVERNMENT, "Government"),
    ]

    donor_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    donor_type = models.CharField(
        max_length=20,
        choices=DONOR_TYPES,
        default=INDIVIDUAL,
    )

    organization = models.CharField(
        max_length=200,
        blank=True,
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    employee_code = models.CharField(
        max_length=50,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ["name"]

    def __str__(self):

        return self.name

    def save(self, *args, **kwargs):

        if not self.donor_id:

            last = Donor.objects.order_by("-id").first()

            if last:

                number = int(last.donor_id.split("-")[1]) + 1

            else:

                number = 1

            self.donor_id = f"DON-{number:04d}"

        super().save(*args, **kwargs)