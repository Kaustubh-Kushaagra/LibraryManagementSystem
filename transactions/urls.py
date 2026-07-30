from django.urls import path

from . import views

urlpatterns = [

    path(
        "issue/<str:accession_number>/",
        views.issue_book,
        name="issue_book",
    ),

    path(
        "return/<int:transaction_id>/",
        views.return_book,
        name="return_book",
    ),

    path(
        "my-books/",
        views.my_books,
        name="my_books",
    ),

    path(
        "manage/",
        views.manage_transactions,
        name="manage_transactions",
    ),

    path(
        "request-return/<int:transaction_id>/",
        views.request_return,
        name="request_return",
    ),

    path(
        "pending-returns/",
        views.pending_returns,
        name="pending_returns",
    ),

    path(
        "approve-return/<int:transaction_id>/",
        views.approve_return,
        name="approve_return",
    ),

]