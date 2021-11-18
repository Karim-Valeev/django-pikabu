from django.urls import path
from django.urls import re_path

from .views import *

urlpatterns = [
    # Root
    path("", main_page, name="main"),
    # Account
    path("register/", registration_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("account/", account_view, name="account"),
    path("account/my-posts/", MyPostsListView.as_view(), name="my-posts"),
    # Posts
    path("posts/", AllPostsListView.as_view(), name="posts"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post"),
    path("posts/create/", CreatePostView.as_view(), name="create-post"),
    path("posts/<int:pk>/update/", UpdatePostView.as_view(), name="update-post"),
    path("posts/<int:pk>/delete/", DeletePostView.as_view(), name="delete-post"),
    # Comments
    re_path(
        r"^posts/(?P<post_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/create$",
        CreateCommentView.as_view(),
        name="create-comment",
    ),
    path("comments/<int:pk>/update/", UpdateCommentView.as_view(), name="update-comment"),
    path("comments/<int:pk>/delete/", DeleteCommentView.as_view(), name="delete-comment"),
]
