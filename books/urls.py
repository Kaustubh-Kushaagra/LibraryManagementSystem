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


    path(
        "ajax/create-author/",
        views.create_author,
        name="create_author",
    ),

    path(
        "ajax/create-publisher/",
        views.create_publisher,
        name="create_publisher",
    ),

    path(
        "ajax/create-category/",
        views.create_category,
        name="create_category",
    ),

    path(
        "ajax/create-donor/",
        views.create_donor,
        name="create_donor",
    ),

]