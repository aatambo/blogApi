import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    """extends custom user model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    about = models.CharField(max_length=254, blank=True)
    country = CountryField(blank_label="(select country)")
    image = models.ImageField(verbose_name="image", upload_to="users/", blank=True)

    EMAIL_FIELD = "email"
