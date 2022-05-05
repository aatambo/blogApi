import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import AccessToken, get_application_model
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()
Application = get_application_model()


# test registration view
class RegistrationViewAPITests(APITestCase):
    """apitest on PUT method"""

    def test_create(self):
        """check put method"""
        client = APIClient()

        url = reverse("users:register")
        data = {
            "username": "testuser",
            "email": "testemail@gmail.com",
            "password": "zzzYYYYabcde12345",
            "password2": "zzzYYYYabcde12345",
        }
        response = client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# test password reset view
class ResetPasswordViewAPITests(APITestCase):
    """apitest on PUT method"""

    @classmethod
    def setUpTestData(cls):
        # create user
        testuser = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com",
            about="clever",
            password="abcde12345",
            first_name="reflex",
            country="KE",
        )
        testuser.save()

    def test_create(self):
        """check put method"""
        client = APIClient()

        url = reverse("users:password-reset")
        data = {
            "email": "testemail@gmail.com",
            "password": "a3e5r6t7y8u90g7v6bt79677bcde09876",
        }
        response = client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# test user list view
class UserListViewAPITests(APITestCase):
    """apitest on GET method"""

    def test_list(self):
        """check get method"""
        client = APIClient()

        url = reverse("users:user-list")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


# test user detail view
class UserDetailViewAPITests(APITestCase):
    """apitest on GET,PUT,PATCH,DELETE method"""

    @classmethod
    def setUpTestData(cls):
        # create user
        testuser = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com",
            about="slave",
            password="abcde12345",
        )
        testuser.save()
        # create dev user
        dev_user = User.objects.create_user(
            username="dev_user",
            email="devemail@gmail.com",
            about="master",
            password="abcde12345",
        )
        dev_user.save()
        # create application for authentication
        application = Application(
            name="Test Application",
            redirect_uris="http://127.0.0.1:8000/noexist/callback",
            user=dev_user,
            client_type="Application.CLIENT_CONFIDENTIAL",
            authorization_grant_type="Application.GRANT_PASSWORD",
        )
        application.save()

    def test_retrieve(self):
        """check get method"""
        client = APIClient()
        # get user
        user = User.objects.get(username="testuser")

        url = reverse("users:user-detail", kwargs={"user_pk": user.id})

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        """check patch method"""
        # get user
        user = User.objects.get(username="testuser")
        # get application
        application = Application.objects.get(name="Test Application")
        # create user token
        access_token = AccessToken.objects.create(
            user=user,
            token="1234567890",
            application=application,
            expires=timezone.now() + datetime.timedelta(days=1),
        )
        # authenticate
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("users:user-detail", kwargs={"user_pk": user.id})
        data = {"first_name": "Kidding"}
        # patch
        response = client.patch(url, data, format="json")
        # logout
        client.credentials()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        """check put method"""
        # get user
        user = User.objects.get(username="testuser")
        # get application
        application = Application.objects.get(name="Test Application")
        # create user token
        access_token = AccessToken.objects.create(
            user=user,
            token="1234567890",
            application=application,
            expires=timezone.now() + datetime.timedelta(days=1),
        )
        # authenticate
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("users:user-detail", kwargs={"user_pk": user.id})
        data = {
            "username": "alkagvcgdvb",
            "first_name": "lalaza",
            "last_name": "chalaza",
            "country": "KE",
            "about": "Nothing",
        }
        # put
        response = client.put(url, data, format="json")
        # logout
        client.credentials()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """check delete method"""
        # get user
        user = User.objects.get(username="testuser")
        # get application
        application = Application.objects.get(name="Test Application")
        # create user token
        access_token = AccessToken.objects.create(
            user=user,
            token="1234567890",
            application=application,
            expires=timezone.now() + datetime.timedelta(days=1),
        )
        # authenticate
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("users:user-detail", kwargs={"user_pk": user.id})
        # delete
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# test user image view
class UserImageViewAPITests(APITestCase):
    """apitest on GET,PUT,PATCH,DELETE method"""

    @classmethod
    def setUpTestData(cls):
        # create user
        testuser = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com",
            about="slave",
            password="abcde12345",
        )
        testuser.save()
        # create dev user
        dev_user = User.objects.create_user(
            username="dev_user",
            email="devemail@gmail.com",
            about="master",
            password="abcde12345",
        )
        dev_user.save()
        # create application for authentication
        application = Application(
            name="Test Application",
            redirect_uris="http://127.0.0.1:8000/noexist/callback",
            user=dev_user,
            client_type="Application.CLIENT_CONFIDENTIAL",
            authorization_grant_type="Application.GRANT_PASSWORD",
        )
        application.save()

    def test_retrieve(self):
        """check get method"""
        client = APIClient()
        # get user
        user = User.objects.get(username="testuser")

        url = reverse("users:user-pic", kwargs={"user_pk": user.id})

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        """check patch method"""
        # get user
        user = User.objects.get(username="testuser")
        # get application
        application = Application.objects.get(name="Test Application")
        # create user token
        access_token = AccessToken.objects.create(
            user=user,
            token="1234567890",
            application=application,
            expires=timezone.now() + datetime.timedelta(days=1),
        )
        # authenticate
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("users:user-pic", kwargs={"user_pk": user.id})
        # open image
        with open("tests_data/user.png", "rb") as image:
            data = {"image": image}
            # put
            response = client.patch(url, data, format="multipart")

        # logout
        client.credentials()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        """check put method"""
        # get user
        user = User.objects.get(username="testuser")
        # get application
        application = Application.objects.get(name="Test Application")
        # create user token
        access_token = AccessToken.objects.create(
            user=user,
            token="1234567890",
            application=application,
            expires=timezone.now() + datetime.timedelta(days=1),
        )
        # authenticate
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("users:user-pic", kwargs={"user_pk": user.id})
        # open image
        with open("tests_data/user.png", "rb") as image:
            data = {"image": image}
            # put
            response = client.put(url, data, format="multipart")

        # logout
        client.credentials()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """check delete method"""
        # get user
        user = User.objects.get(username="testuser")
        # get application
        application = Application.objects.get(name="Test Application")
        # create user token
        access_token = AccessToken.objects.create(
            user=user,
            token="1234567890",
            application=application,
            expires=timezone.now() + datetime.timedelta(days=1),
        )
        # authenticate
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("users:user-pic", kwargs={"user_pk": user.id})
        # delete
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
