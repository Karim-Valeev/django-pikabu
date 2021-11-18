from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from main.forms import PostForm
from main.mixins import OwnershipRequiredMixin
from main.models import Post


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "main/post/createPost.html"

    def get_success_url(self):
        return reverse_lazy("my-posts")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdatePostView(LoginRequiredMixin, OwnershipRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "main/post/updatePost.html"

    def get_success_url(self):
        return reverse_lazy("post", kwargs={"pk": self.get_object().pk})


class DeletePostView(LoginRequiredMixin, OwnershipRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("my-posts")


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "main/post/singlePost.html"


class AllPostsListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "main/post/allPosts.html"

    def get_queryset(self):
        return Post.objects.all().select_related("author").prefetch_related("comments", "categories")


class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "main/post/accountPosts.html"

    def get_queryset(self):
        return (
            Post.objects.filter(author=self.request.user)
            .select_related("author")
            .prefetch_related("comments", "categories")
        )
