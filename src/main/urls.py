from django.urls import path

from .views import *

urlpatterns = [
    # Root
    path("", main_page, name="main"),
    # Account
    path("register/", registration_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("account/", account_view, name="account"),
    path("account/my-posts/", main_page, name="my-posts"),
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
]
