from django.urls import path
from . import views

urlpatterns = [

    path(
        "read/<int:pk>/",
        views.read_notification,
        name="read_notification",
    ),

]