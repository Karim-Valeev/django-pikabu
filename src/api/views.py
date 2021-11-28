from main.models import Comment
from main.models import Post
from main.models import User
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .mixins import ChangeOnlyForOwnerPermission
from .serializers import CommentSerializer
from .serializers import PostCreateSerializer
from .serializers import PostSerializer
from .serializers import PostUpdateSerializer
from .serializers import UserCreateSerializer
from .serializers.comment import CommentCreateSerializer
from .serializers.comment import CommentUpdateSerializer


@api_view(["GET"])
def check_api_view(request):
    """Method for checking api"""
    content = {"status": "ok"}
    return Response(content, status=status.HTTP_200_OK)


class UserCreateView(generics.CreateAPIView):
    """User creation via API"""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


# Todo Стоит ли общие поля и значения вынести в какой-то BaseModelViewSet?
class PostViewSet(ModelViewSet):
    """Posts"""

    permission_classes = [IsAuthenticated, ChangeOnlyForOwnerPermission]
    serializer_class = PostSerializer
    # Фильтрация по айдишнику пользователя
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["created_at"]
    search_fields = ["author__id"]

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostSerializer
        if self.action == "create":
            return PostCreateSerializer
        if self.action == "update":
            return PostUpdateSerializer
        return PostSerializer

    def get_queryset(self):
        return Post.objects.all()


class CommentViewSet(ModelViewSet):
    """Comments"""

    permission_classes = [IsAuthenticated, ChangeOnlyForOwnerPermission]
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["created_at"]
    search_fields = ["post__id", "author__username"]

    def create(self, request, *args, **kwargs):
        comment_id = int(request.POST.get("in_reply_to", ""))
        in_reply_to: Comment = Comment.objects.first(pk=comment_id)
        # т.к. здесь сложное логическое условие решил исппользовать флаг
        flag = True
        if in_reply_to is not None:
            flag = in_reply_to.is_replying_allowed
        if flag:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"Error message": f"Your are not allowed to reply to comment with id {comment_id}"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CommentSerializer
        if self.action == "create":
            return CommentCreateSerializer
        if self.action == "update":
            return CommentUpdateSerializer
        return CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
