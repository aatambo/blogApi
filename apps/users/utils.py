import six
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
reset_password_token = TokenGenerator()


def send_email_confirm_account(user, request):
    domain = request.get_host()
    subject = "Activate Your Account"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    message = render_to_string(
        "account_activation_email.html",
        {
            "user": user,
            "domain": domain,
            "uid": uid,
            "token": token,
            "expiry": settings.PASSWORD_RESET_TIMEOUT_DAYS,
        },
    )
    user.email_user(subject, message)


def send_email_reset_password(user, request):
    domain = request.get_host()
    subject = "Confirm Password Reset"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = reset_password_token.make_token(user)
    message = render_to_string(
        "password_reset_email.html",
        {
            "user": user,
            "domain": domain,
            "uid": uid,
            "token": token,
            "expiry": settings.PASSWORD_RESET_TIMEOUT_DAYS,
        },
    )
    user.email_user(subject, message)
