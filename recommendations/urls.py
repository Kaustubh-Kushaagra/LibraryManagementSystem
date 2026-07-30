from django.urls import path
from . import views

urlpatterns = [

    path(
        "manage/",
        views.recommendation_list,
        name="recommendation_list",
    ),

    path(
        "",
        views.recommend_book,
        name="recommend_book",
    ),

    path(
        "manage/<int:pk>/",
        views.recommendation_detail,
        name="recommendation_detail",
    ),

    path(
        "manage/<int:pk>/approve/",
        views.approve_recommendation,
        name="approve_recommendation",
    ),

    path(
        "manage/<int:pk>/reject/",
        views.reject_recommendation,
        name="reject_recommendation",
    ),

    path(
        "my/",
        views.my_recommendations,
        name="my_recommendations",
    ),
   

]