from django.urls import path
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from .views import check_api_view
from .views import CommentViewSet
from .views import PostViewSet
from .views import UserCreateView


router = SimpleRouter()
router.register("posts", PostViewSet, "posts-api")
router.register("comments", CommentViewSet, "comments-api")
# .../posts with url_name posts-api-list
# .../posts/id with url_name posts-api-detail

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="1.0.0",
        description="API for working with the test django forum",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="karim.valeev.i@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path("check/", check_api_view, name="check-api"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token-refresh"),
    path("register/", UserCreateView.as_view(), name="api-register"),
    *router.urls,
    re_path(
        "swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
