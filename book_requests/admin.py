from django.contrib import admin
from .models import BookRequest


@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):

    list_display = (
        "book",
        "member",
        "status",
        "requested_at",
        "pickup_date",
        "pickup_time",
    )

    list_filter = (
        "status",
        "requested_at",
    )

    search_fields = (
        "book__title",
        "book__accession_number",
        "member__username",
        "member__first_name",
        "member__last_name",
    )

    ordering = (
        "-requested_at",
    )