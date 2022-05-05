from django.urls import path

from .views import CommentDetailView, CommentListView, PostDetailView, PostListView

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<post_pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<post_pk>/comments/", CommentListView.as_view(), name="comment-list"),
    path(
        "posts/<post_pk>/comments/<comment_pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
]
