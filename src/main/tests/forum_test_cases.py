from api.views import check_api_view
from django.test import RequestFactory
from django.test import TestCase
from main.models import User


class ForumApiChechTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = User(email="test2@gmail.ru", username="Тестер2")
        user.set_password("password2")
        user.save()
        self.user = user

    def test_api_check(self):
        request = self.factory.get("/api/check/")
        response = check_api_view(request)
        data = response.data
        self.assertEqual("ok", data["status"])
