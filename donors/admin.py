from django.contrib import admin
from .models import Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):

    list_display = (
        "donor_id",
        "name",
        "organization",
        "phone",
        "email",
    )

    search_fields = (
        "donor_id",
        "name",
        "organization",
    )

    ordering = (
        "name",
    )