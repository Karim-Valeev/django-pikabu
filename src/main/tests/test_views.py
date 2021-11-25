import pytest
from main.models import User


@pytest.fixture
def create_user(db):
    def make_user():
        return User.objects.create(email="test@test.com", username="tester", password="test_password")

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user):
    def make_auto_login():
        user = create_user()
        client.login(email=user.email, password=user.password)
        return client, user

    return make_auto_login


# @pytest.mark.django_db
# def test_log_in_incorrect_data(client):
#     response = client.post("/login", {"email": "test@test.test", "password": "incorrect"})
#     assert response.url == "/sign_in/"
