from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
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
        try:
            comment = Comment.objects.get(pk=self.kwargs["comment_id"])
        except Comment.DoesNotExist:
            comment = None
        context["comment"] = comment
        return context

    def form_valid(self, form):
        try:
            in_reply_to = Comment.objects.get(pk=self.kwargs["comment_id"])
        except Comment.DoesNotExist:
            in_reply_to = None
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        comment.in_reply_to = in_reply_to
        # т.к. здесь сложное логическое условие решил исппользовать флаг
        flag = True
        if in_reply_to is not None:
            flag = in_reply_to.is_replying_allowed
        if flag:
            comment.save()
        return HttpResponseRedirect(self.get_success_url())

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
