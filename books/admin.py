from django.contrib import admin
from .models import Category, Author, Publisher, Donor, LibraryItem


# ---------------------------
# Category
# ---------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# ---------------------------
# Author
# ---------------------------

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# ---------------------------
# Publisher
# ---------------------------

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)
    ordering = ("name",)



# ---------------------------
# Library Item
# ---------------------------

@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):

    list_display = (
        "accession_number",
        "title",
        "author",
        "category",
        "status",
        "location",
        "acquisition_type",
    )

    search_fields = (
        "accession_number",
        "title",
        "author__name",
        "publisher__name",
        "location",
    )

    list_filter = (
        "status",
        "category",
        "publisher",
        "acquisition_type",
    )

    ordering = (
        "title",
        "accession_number",
    )

    list_per_page = 25

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        ("Book Information", {
            "fields": (
                "accession_number",
                "title",
                "author",
                "publisher",
                "category",
            )
        }),

        ("Publication", {
            "fields": (
                "publication_year",
                "pages",
                "price",
                "volume_qty",
            )
        }),

        ("Acquisition", {
            "fields": (
                "acquisition_type",
                "donor",
            )
        }),

        ("Library Details", {
            "fields": (
                "location",
                "status",
                "remarks",
            )
        }),

        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )