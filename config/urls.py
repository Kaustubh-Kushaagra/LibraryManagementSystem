from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from accounts.forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [

    path("", RedirectView.as_view(url="/login/", permanent=False)),

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("accounts.urls"),
    ),

    path(
        "",
        include("books.urls"),
    ),

    path(
        "",
        include("transactions.urls"),
    ),

    path(
        "imports/",
        include("imports.urls"),
    ),

    path(
        "reports/",
        include("reports.urls"),
    ),

    path(
        "administration/",
        include("administration.urls"),
    ),

    path(
        "requests/",
        include("book_requests.urls"),
    ),

    path(
        "notifications/",
        include("notifications.urls"),
    ),

    path(
        "recommendations/",
        include("recommendations.urls"),
    ),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name="registration/password_reset.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            form_class=CustomSetPasswordForm,
            template_name="registration/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )