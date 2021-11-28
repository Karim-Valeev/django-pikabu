import pytest
from django.urls import reverse
from main.models import Comment
from main.models import Post


@pytest.fixture
def get_password():
    return "Test_pass.2021"


@pytest.fixture
def create_user(db, django_user_model, get_password):
    def make_user(**kwargs):
        kwargs["password"] = get_password
        if "email" not in kwargs:
            kwargs["email"] = "test@test.com"
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, get_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(email=user.email, password=get_password)
        return client, user

    return make_auto_login


@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse("my-posts")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse("logout")
    response = client.get(url)
    assert response.url == "/"


@pytest.mark.django_db
def test_create_post_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse("create-post")
    client.post(url, {"title": "Test post", "body": "Test post body :)"})
    new_post = Post.objects.get(title="Test post")
    assert new_post.body == "Test post body :)"


@pytest.mark.django_db
def test_delete_post(auto_login_user):
    client, user = auto_login_user()
    create_url = reverse("create-post")
    client.post(create_url, {"title": "Test post", "body": "Test post body :)"})
    new_post_pk = Post.objects.get(title="Test post").pk
    delete_url = reverse("delete-post", kwargs={"pk": new_post_pk})
    response = client.post(delete_url)
    assert response.url == reverse("my-posts")


@pytest.mark.django_db
def test_leave_comment_under_other_comment(auto_login_user):
    client, user = auto_login_user()
    create_post_url = reverse("create-post")
    client.post(create_post_url, {"title": "Test post", "body": "Test post body :)"})
    post_id = Post.objects.get(title="Test post").pk
    create_first_comment_url = reverse(
        "create-comment", kwargs={"post_id": post_id, "comment_id": 0}
    )
    client.post(create_first_comment_url, {"text": "First comment under first post"})
    first_comment_id = Comment.objects.get(author=user).pk
    create_first_reply_comment_url = reverse(
        "create-comment", kwargs={"post_id": post_id, "comment_id": first_comment_id}
    )
    client.post(create_first_reply_comment_url, {"text": "First reply to comment"})
    first_reply_comment: Comment = Comment.objects.get(in_reply_to__pk=first_comment_id)
    assert first_reply_comment.in_reply_to.pk == first_comment_id
