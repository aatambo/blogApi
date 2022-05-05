from django.urls import path

from .views import (
    RegistrationEmailVerificationView,
    RegistrationView,
    ResetPasswordEmailVerificationView,
    ResetPasswordView,
    UserDetailView,
    UserImageView,
    UserListView,
)

app_name = "users"

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<user_pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<user_pk>/pic/", UserImageView.as_view(), name="user-pic"),
    path("registration/", RegistrationView.as_view(), name="register"),
    path(
        "activate/<uidb64>/<token>/",
        RegistrationEmailVerificationView.as_view(),
        name="activate",
    ),
    path("password_reset/", ResetPasswordView.as_view(), name="password-reset"),
    path(
        "password_verify/<uidb64>/<token>/",
        ResetPasswordEmailVerificationView.as_view(),
        name="password-verify",
    ),
]
