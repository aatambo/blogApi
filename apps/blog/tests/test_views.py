import datetime

from blog.models import Comment, Post
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import AccessToken, get_application_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()
Application = get_application_model()


# test postlist View
class PostListViewAPITests(APITestCase):
    """APITests on GET and POST"""

    @classmethod
    def setUpTestData(cls):
        # create user
        testuser = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com",
            about="stupid",
            password="abcde12345",
        )
        testuser.save()
        # create dev user
        dev_user = User.objects.create_user(
            username="dev_user",
            email="devemail@gmail.com",
            about="king",
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

    def test_list(self):
        """check get method on post list"""
        client = APIClient()

        url = reverse("blog:post-list")
        response = client.get(url, format="json")

        # anyone can see a post list, including anonymous users
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        """check post method on post list"""
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
        # url and data
        url = reverse("blog:post-list")
        data = {
            "author": user.username,
            "title": "Praise Jesus Christ",
            "body": "Amen!",
        }
        # post method
        response = client.post(url, data, format="json")
        # logout
        client.credentials()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# test postdetail View
class PostDetailViewAPITests(APITestCase):
    """APITests on GET,PATCH,PUT,DELETE"""

    @classmethod
    def setUpTestData(cls):
        # create user
        testuser = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com",
            about="stupid",
            password="abcde12345",
        )
        testuser.save()
        # create dev user
        dev_user = User.objects.create_user(
            username="dev_user",
            email="devemail@gmail.com",
            about="king",
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
        # create post
        testpost = Post.objects.create(
            author=testuser,
            title="Hello World!",
            body="How to hack NASA with html",
        )
        testpost.save()
        # store id to a variable since it is a uuid
        global testpost_id
        testpost_id = testpost.id

    def test_retrieve(self):
        """check get method on post detail"""
        client = APIClient()
        # get post
        post = Post.objects.get(id=testpost_id)

        url = reverse("blog:post-detail", kwargs={"post_pk": post.id})
        response = client.get(url, format="json")

        # anyone can see post detail, including anonymous users
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        """check patch method on post detail"""
        # get user
        user = User.objects.get(username="testuser")
        # get post
        post = Post.objects.get(id=testpost_id)
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
        # proceed to update post
        url = reverse("blog:post-detail", kwargs={"post_pk": post.id})
        data = {"body": "Just kidding"}
        # patch method allows update on partial data
        response = client.patch(url, data, format="json")
        # logout
        client.credentials()

        # patch post response should be OK since obj.author == request.user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get post after update
        post = Post.objects.get(id=testpost_id)
        body = f"{post.body}"

        # check the new body against the update value passed eearlier
        self.assertEqual(body, data["body"])

    def test_update(self):
        """check put method on post detail"""
        # get user
        user = User.objects.get(username="testuser")
        # get post
        post = Post.objects.get(id=testpost_id)
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
        # proceed to update post
        url = reverse("blog:post-detail", kwargs={"post_pk": post.id})
        data = {"title": "This is is tiresome!", "body": "Just kidding"}
        # patch method allows update on partial data
        response = client.put(url, data, format="json")
        # logout
        client.credentials()

        # patch post response should be OK since obj.author == request.user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get post after update
        post = Post.objects.get(id=testpost_id)
        body = f"{post.body}"

        # check the new body against the update value passed eearlier
        self.assertEqual(body, data["body"])

    def test_delete(self):
        """check delete method on post detail"""
        # get user
        user = User.objects.get(username="testuser")
        # get post
        post = Post.objects.get(id=testpost_id)
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
        url = reverse("blog:post-detail", kwargs={"post_pk": post.id})
        # delete
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# test commentlist View
class CommentListViewAPITests(APITestCase):
    """APITests on GET and POST"""

    @classmethod
    def setUpTestData(cls):
        # create user
        testuser = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com",
            about="stupid",
            password="abcde12345",
        )
        testuser.save()
        # create dev user
        dev_user = User.objects.create_user(
            username="dev_user",
            email="devemail@gmail.com",
            about="king",
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
        # create post
        testpost = Post.objects.create(
            author=testuser,
            title="Hello World!",
            body="How to hack NASA with html",
        )
        testpost.save()
        # store id to a variable since it is a uuid
        global testpost_id
        testpost_id = testpost.id

    def test_list(self):
        """check get method on comment list"""
        # get post
        post = Post.objects.get(id=testpost_id)
        client = APIClient()
        # url and data
        url = reverse("blog:comment-list", kwargs={"post_pk": post.id})
        response = client.get(url, format="json")

        # anyone can see a comment list, including anonymous users
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        """check post method on comment list"""
        # get user
        user = User.objects.get(username="testuser")
        # get application
        application = Application.objects.get(name="Test Application")
        # get post
        post = Post.objects.get(id=testpost_id)
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
        # url and data
        url = reverse("blog:comment-list", kwargs={"post_pk": post.id})
        data = {
            "body": "Amen!",
        }
        # post method
        response = client.post(url, data, format="json")
        # logout
        client.credentials()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# test commentdetail View
class CommentDetailViewAPITests(APITestCase):
    """APITests on GET,PATCH,PUT,DELETE"""

    @classmethod
    def setUpTestData(cls):
        # create user
        testuser = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com",
            about="stupid",
            password="abcde12345",
        )
        testuser.save()
        # create dev user
        dev_user = User.objects.create_user(
            username="dev_user",
            email="devemail@gmail.com",
            about="king",
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
        # create post
        testpost = Post.objects.create(
            author=testuser,
            title="Hello World!",
            body="How to hack NASA with html",
        )
        testpost.save()
        # store id to a variable since it is a uuid
        global testpost_id
        testpost_id = testpost.id
        # create comment
        testcomment = Comment.objects.create(
            author=testuser,
            post=testpost,
            body="So?",
        )
        testcomment.save()
        # store id to a variable since it is a uuid
        global testcomment_id
        testcomment_id = testcomment.id

    def test_retrieve(self):
        """check get method on comment detail"""
        client = APIClient()
        # get post
        post = Post.objects.get(id=testpost_id)
        # get comment
        comment = Comment.objects.get(id=testcomment_id)

        url = reverse(
            "blog:comment-detail",
            kwargs={"comment_pk": comment.id, "post_pk": post.id},
        )
        response = client.get(url, format="json")

        # anyone can see comment detail, including anonymous users
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        """check patch method on comment detail"""
        # get user
        user = User.objects.get(username="testuser")
        # get post
        post = Post.objects.get(id=testpost_id)
        # get comment
        comment = Comment.objects.get(id=testcomment_id)
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
        # proceed to update comment
        url = reverse(
            "blog:comment-detail", kwargs={"comment_pk": comment.id, "post_pk": post.id}
        )

        data = {"body": "Just kidding"}
        # patch method allows update on partial data
        response = client.patch(url, data, format="json")

        client.credentials()

        # patch comment response should be OK since obj.author == request.user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get comment after update
        comment = Comment.objects.get(id=testcomment_id)
        body = f"{comment.body}"

        # check the new body against the update value passed eearlier
        self.assertEqual(body, data["body"])

    def test_update(self):
        """check put method on comment detail"""
        # get user
        user = User.objects.get(username="testuser")
        # get post
        post = Post.objects.get(id=testpost_id)
        # get comment
        comment = Comment.objects.get(id=testcomment_id)
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
        # proceed to update comment
        url = reverse(
            "blog:comment-detail", kwargs={"comment_pk": comment.id, "post_pk": post.id}
        )

        data = {"body": "Just kidding"}
        # put method allows update on partial data
        response = client.put(url, data, format="json")

        client.credentials()

        # put comment response should be OK since obj.author == request.user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get comment after update
        comment = Comment.objects.get(id=testcomment_id)
        body = f"{comment.body}"

        # check the new body against the update value passed eearlier
        self.assertEqual(body, data["body"])

    def test_delete(self):
        """check delete method on comment detail"""
        # get user
        user = User.objects.get(username="testuser")
        # get post
        post = Post.objects.get(id=testpost_id)
        # get comment
        comment = Comment.objects.get(id=testcomment_id)
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
        url = reverse(
            "blog:comment-detail", kwargs={"comment_pk": comment.id, "post_pk": post.id}
        )
        # delete
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
