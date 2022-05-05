from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserListSerializer(serializers.ModelSerializer):
    """serializer for user endpoint"""

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
        )


class UserImageSerializer(serializers.ModelSerializer):
    """serializer for user endpoint"""

    class Meta:
        model = get_user_model()
        fields = ("image",)


class UserDetailSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "country",
            "about",
            "image",
        )
        read_only_fields = ["id", "email", "image"]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializers registers and creates a new user."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords did not match"})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )

        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()

        return user


class ResetPasswordSerializer(serializers.ModelSerializer):
    """reset password"""

    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs["email"]).exists():
            return attrs

        raise serializers.ValidationError(
            {"error": "credentials do not match any user account!"}
        )

    def save(self):
        user = get_user_model().objects.get(
            email=self.validated_data["email"],
        )
        password = self.validated_data["password"]

        user.set_password(password)
        user.is_active = False
        user.save()

        return user
