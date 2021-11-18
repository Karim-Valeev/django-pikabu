from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from .views import check_api_view
from .views import CommentViewSet
from .views import PostViewSet
from .views import UserCreate

router = SimpleRouter()
router.register("posts", PostViewSet, "posts")
router.register("comments", CommentViewSet, "comments")
# .../posts
# .../posts/id

urlpatterns = [
    path("check/", check_api_view),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreate.as_view()),
    *router.urls,
]
