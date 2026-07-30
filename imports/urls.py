from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.import_home,
        name="import_home",
    ),

    path(
        "excel/",
        views.upload_excel,
        name="upload_excel",
    ),

    path(
        "preview/<int:import_id>/",
        views.preview_import,
        name="preview_import",
    ),

    path(
        "perform/<int:import_id>/",
        views.perform_import,
        name="perform_import",
    ),

    path(
        "manual/",
        views.manual_book_add,
        name="manual_book_add",
    ),


]