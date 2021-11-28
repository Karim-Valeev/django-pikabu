import pytest
from django.urls import reverse
from main.models import Post
from main.tests import create_user
from main.tests import get_password
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


# хоть здесь казалось бы и нет подключения к БД,
# без метки mark.db тест упадет с RuntimeError: Database access not allowed
@pytest.mark.django_db
def test_unauthorized_check_api_request(api_client):
    url = reverse("check-api")
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthorized_posts_request(api_client):
    url = reverse("posts-api-list")
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_api_user_registation(api_client, get_password):
    url = reverse("api-register")
    response = api_client.post(url, {"email": "new_email@test.com", "password": get_password})
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_access_token(api_client, create_user, get_password):
    user = create_user()
    url = reverse("token-obtain-pair")
    response = api_client.post(url, {"email": user.email, "password": get_password})
    assert "access" in response.data


@pytest.fixture
def get_jwt_access_token_with_auth_header_types(api_client, create_user, get_password):
    user = create_user()
    access_token = api_client.post(
        reverse("token-obtain-pair"), {"email": user.email, "password": get_password}
    ).data["access"]
    access_token_with_header_type = f"Bearer {access_token}"
    return access_token_with_header_type


@pytest.mark.django_db
def test_authorized_posts_request(api_client, get_jwt_access_token_with_auth_header_types):
    url = reverse("posts-api-list")
    api_client.credentials(HTTP_AUTHORIZATION=get_jwt_access_token_with_auth_header_types)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_swagger_documentation(api_client):
    url = reverse("schema-swagger-ui")
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_create_post(api_client, get_jwt_access_token_with_auth_header_types):
    url = reverse("posts-api-list")
    api_client.credentials(HTTP_AUTHORIZATION=get_jwt_access_token_with_auth_header_types)
    response = api_client.post(
        url, {"title": "First post created with api", "body": "Body of first api post 123"}
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_api_delete_post(api_client, get_jwt_access_token_with_auth_header_types):
    api_client.credentials(HTTP_AUTHORIZATION=get_jwt_access_token_with_auth_header_types)
    api_client.post(
        reverse("posts-api-list"),
        {"title": "First post created with api", "body": "Body of first api post 123"},
    )
    post = Post.objects.get(title="First post created with api")
    url = reverse("posts-api-detail", kwargs={"pk": post.pk})
    response = api_client.delete(url)
    assert response.status_code == 204


# 9 создать коммент


# 10 поменять коммент
