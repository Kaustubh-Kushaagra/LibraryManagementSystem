from django.urls import path

from . import views

urlpatterns = [

    path(
        "catalog/",
        views.catalog,
        name="catalog",
    ),

    path(
            "catalog/search/",
            views.search_books,
            name="search_books",
        ),
    

    path(
        "catalog/<str:accession_number>/",
        views.book_detail,
        name="book_detail",
    ),

    path(
        "edit/<str:accession_number>/",
        views.edit_book,
        name="edit_book",
    ),

    path(
        "delete/<str:accession_number>/",
        views.delete_book,
        name="delete_book",
    ),

    

]