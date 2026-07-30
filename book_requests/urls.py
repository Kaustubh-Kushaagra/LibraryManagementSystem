from django.urls import path
from . import views

urlpatterns = [

    path(
        "request/<str:accession_number>/",
        views.request_book,
        name="request_book",
    ),

    path(
        "pending/",
        views.pending_requests,
        name="pending_requests",
    ),

    path(
        "approve/<int:request_id>/",
        views.approve_request,
        name="approve_request",
    ),

    path(
        "confirm/<int:request_id>/",
        views.confirm_collection,
        name="confirm_collection",
    ),

    path(
        "reject/<int:pk>/",
        views.reject_request,
        name="reject_request",
    ),

    path(
        "collect/<int:request_id>/",
        views.collect_book,
        name="collect_book",
    ),    

]