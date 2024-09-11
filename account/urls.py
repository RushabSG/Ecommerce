from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("register", views.register, name="register"),
    # Email Verification URL's
    path(
        "email-verification/<str:uidb64>/<str:token>/",
        views.email_verification,
        name="email-verification",
    ),
    path(
        "email-verification-sent",
        views.email_verification_sent,
        name="email-verification-sent",
    ),
    path(
        "email-verification-success",
        views.email_verification_success,
        name="email-verification-success",
    ),
    path(
        "email-verification-failed",
        views.email_verification_failed,
        name="email-verification-failed",
    ),
    # login / logout urls
    path(
        "login",
        views.my_login,
        name="login",
    ),
    path(
        "logout",
        views.user_logout,
        name="logout",
    ),
    # dashboard
    path(
        "dashboard",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "dashboard",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "profile-management",
        views.profile_management,
        name="profile-management",
    ),
    path(
        "delete-account",
        views.delete_account,
        name="delete-account",
    ),
    # password reset
    # submit our email form
    path(
        "password-reset/",
        PasswordResetView.as_view(template_name="account/password/password-reset.html"),
        name="password-reset",
    ),
    # for password reset email
    path(
        "password-reset-sent/",
        PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    # password reset link
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    # success message, password was reset
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    # shipping url
    path("manage-shipping/", views.manage_shipment, name="manage-shipping"),
    # order management
    path("track-order/", views.track_order, name="track-order"),
]
