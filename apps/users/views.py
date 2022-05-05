from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .permissions import IsUserOrReadOnly
from .serializers import (
    RegisterSerializer,
    ResetPasswordSerializer,
    UserDetailSerializer,
    UserImageSerializer,
    UserListSerializer,
)
from .utils import (
    account_activation_token,
    reset_password_token,
    send_email_confirm_account,
    send_email_reset_password,
)


class UserListView(generics.ListAPIView):
    """Lists users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update, Delete user details"""

    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsUserOrReadOnly,)
    lookup_url_kwarg = "user_pk"


class UserImageView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update, Delete user details"""

    queryset = get_user_model().objects.all()
    serializer_class = UserImageSerializer
    permission_classes = (IsUserOrReadOnly,)
    parser_classes = [MultiPartParser, FormParser]
    lookup_url_kwarg = "user_pk"

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.save()


class RegistrationView(generics.GenericAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = get_user_model().objects.get(username=serializer.data["username"])
        send_email_confirm_account(user, request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationEmailVerificationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Thank you for your email confirmation!")
        else:
            if user is not None:
                if user.is_active == False:
                    user.delete()
                    return HttpResponse(
                        f"""
                        Activation link is invalid! Possibly it has expired!
                        Email confirmation failed
                        User {{user.username}} has been deleted.
                        Register again!
                        """
                    )
                else:
                    return HttpResponse("Activation link is invalid!")
            else:
                return HttpResponse("Activation link is invalid!")


class ResetPasswordView(generics.GenericAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = get_user_model().objects.get(email=serializer.data["email"])
        send_email_reset_password(user, request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResetPasswordEmailVerificationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and reset_password_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Password Changed Successfully!")
        else:
            return HttpResponse("Activation link is invalid!")
