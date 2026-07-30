from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import views
from accounts.forms import CustomAuthenticationForm


urlpatterns = [

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # Members
    path(
        "members/",
        views.member_list,
        name="member_list",
    ),

    path(
        "members/<int:user_id>/",
        views.member_detail,
        name="member_detail",
    ),

    path(
        "members/<int:user_id>/toggle/",
        views.toggle_member_status,
        name="toggle_member_status",
    ),

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile",
    ),

    path(
        "profile/change-password/",
        PasswordChangeView.as_view(
            template_name="accounts/change_password.html"
        ),
        name="change_password",
    ),

    path(
        "profile/change-password/done/",
        PasswordChangeDoneView.as_view(
            template_name="accounts/change_password_done.html"
        ),
        name="password_change_done",
    ),

    path(
        "members/<int:user_id>/reset-password/",
        views.reset_member_password,
        name="reset_member_password",
    ),

    path(
        "members/password-reset-success/",
        views.password_reset_success,
        name="password_reset_success",
    ),

]