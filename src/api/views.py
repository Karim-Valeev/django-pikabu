from main.models import Post
from main.models import User
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import PostCreateSerializer
from .serializers import PostSerializer
from .serializers import PostUpdateSerializer
from .serializers import UserCreateSerializer


@api_view(["GET"])
def check_api_view(request):
    """Method for checking api"""
    content = {"status": "ok"}
    return Response(content, status=status.HTTP_200_OK)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class PostViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

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
        # user = self.request.user
        # return Post.objects.filter(author=user)
        return Post.objects.all()


# class NoteChangeOnlyForOwnerPermission(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.author.id == request.user.id
#
#
# class NoteViewSet(ModelViewSet):
#     """Notes"""
#     permission_classes = [IsAuthenticated, NoteChangeOnlyForOwnerPermission]
#     serializer_class = NoteSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["topic"]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer: NoteSerializer):
#         author = self.request.user
#         instance: Note = serializer.save(author=author)
#         # todo брать URL из настроек
#         url = f"http://127.0.0.1:8000/notes/{instance.id}"
#         instance.url = url
#         instance.save()
#
#     def get_serializer_class(self):
#         if self.action == "retrieve":
#             return NoteSerializer
#         if self.action == "create":
#             return NoteCreateSerializer
#         if self.action == "update":
#             return NoteUpdateSerializer
#         return NoteSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return Note.objects.filter(author=user)
