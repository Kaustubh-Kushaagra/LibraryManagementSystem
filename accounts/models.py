from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    HEAD_LIBRARIAN = "head_librarian"
    LIBRARY_HELPER = "library_helper"
    MEMBER = "member"

    ROLE_CHOICES = [
        (HEAD_LIBRARIAN, "Head Librarian"),
        (LIBRARY_HELPER, "Library Helper"),
        (MEMBER, "Member"),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=MEMBER,
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.employee_id:
            return f"{self.employee_id} - {self.get_full_name() or self.username}"
        return self.username