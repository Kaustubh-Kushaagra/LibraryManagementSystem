from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "book",
        "member",
        "issued_at",
        "due_date",
        "status",
    )

    search_fields = (
        "book__title",
        "book__accession_number",
        "member__username",
        "member__first_name",
        "member__last_name",
    )

    list_filter = (
        "status",
        "issued_at",
        "due_date",
    )

    readonly_fields = (
        "issued_at",
        "returned_at",
    )

    ordering = (
        "-issued_at",
    )