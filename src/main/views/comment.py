from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from main.forms import CommentForm
from main.mixins import OwnershipRequiredMixin
from main.models import Comment
from main.models import Post


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "main/comment/createComment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["post_id"])
        # здесь как бы нарушение DRY, стоит ли вынести в отдельный метод и в отдельный файлик?
        comments = Comment.objects.filter(id=self.kwargs["comment_id"])
        context["comment"] = comments[0] if len(comments) == 1 else None
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        comments = Comment.objects.filter(id=self.kwargs["comment_id"])
        comment.in_reply_to = comments[0] if len(comments) == 1 else None
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post", kwargs={"pk": self.kwargs["post_id"]})


class UpdateCommentView(LoginRequiredMixin, OwnershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "main/comment/updateComment.html"

    def get_success_url(self):
        return reverse_lazy("post", kwargs={"pk": self.get_object().post.pk})


class DeleteCommentView(LoginRequiredMixin, OwnershipRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy("post", kwargs={"pk": self.get_object().post.pk})
