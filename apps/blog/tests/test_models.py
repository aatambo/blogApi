from blog.models import Comment, Post
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

# test post model
class PostModelTest(TestCase):
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
        # create post
        testpost = Post.objects.create(
            author=testuser,
            title="Hello World!",
            body="body content...",
        )
        testpost.save()
        # store id to a variable since it is a uuid
        global testpost_id
        testpost_id = testpost.id

    def test_post_content(self):
        post = Post.objects.get(id=testpost_id)
        author = f"{post.author}"
        title = f"{post.title}"
        body = f"{post.body}"

        # checks
        self.assertEqual(author, "testuser")
        self.assertEqual(title, "Hello World!")
        self.assertEqual(body, "body content...")


# test comment model
class CommentModelTest(TestCase):
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
        # create post
        testpost = Post.objects.create(
            author=testuser,
            title="Hello World!",
            body="My first post, na hutaniambia kitu",
        )
        testpost.save()
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

    def test_comment_content(self):
        comment = Comment.objects.get(id=testcomment_id)
        author = f"{comment.author}"
        post = f"{comment.post}"
        body = f"{comment.body}"

        # checks
        self.assertEqual(author, "testuser")
        self.assertEqual(post, "Hello World!")
        self.assertEqual(body, "So?")
