from django.urls import path
from django.urls import re_path

from src.main.views import main_page

urlpatterns = [
    path("", main_page, name=""),
    # Account
    path("account/register/", main_page, name="register"),
    path("account/login/", main_page, name="login"),
    path("account/logout/", main_page, name="logout"),
    path("account/", main_page, name="account"),
    path("account/my-posts/", main_page, name=""),
    # Posts
    path("posts/", main_page, name=""),
    path("posts/<int:post_id>/", main_page, name=""),
    path("posts/create/", main_page, name=""),
    path("posts/<int:post_id>/udate/", main_page, name=""),
    path("posts/<int:post_id>/delete/", main_page, name=""),
    # Comments
    path("posts/<int:post_id>/comments/create/", main_page, name=""),
    path("posts/<int:post_id>/comments/<int:comment_id>/update/", main_page, name=""),
    path("posts/<int:post_id>/comments/<int:comment_id>/delete/", main_page, name=""),
    # REST API:
    # ...
]
