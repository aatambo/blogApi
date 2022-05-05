from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

# test user model
class UserModelTest(TestCase):
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

    def test_user_content(self):
        user = User.objects.get(username="testuser")
        username = f"{user.username}"
        email = f"{user.email}"
        first_name = f"{user.first_name}"
        last_name = f"{user.last_name}"
        password = f"{user.password}"
        about = f"{user.about}"
        country = f"{user.country}"
        image = f"{user.image}"

        # checks
        self.assertEqual(username, "testuser")
        self.assertEqual(email, "testemail@gmail.com")
        self.assertEqual(first_name, "reflex")
        self.assertEqual(last_name, "")
        self.assertEqual(about, "clever")
        self.assertEqual(country, "KE")
        self.assertEqual(image, "")
