from django.urls import path

from . import views

urlpatterns = [

    path(
        "books/",
        views.export_books_excel,
        name="export_books_excel",
    ),

    path(
        "members/",
        views.export_members_excel,
        name="export_members_excel",
    ),

    path(
        "issued/",
        views.export_issued_books_excel,
        name="export_issued_books_excel",
    ),


    path(
        "overdue/",
        views.export_overdue_books_excel,
        name="export_overdue_books_excel",
    ),

    path(
        "",
        views.reports_home,
        name="reports_home",
    ),

]