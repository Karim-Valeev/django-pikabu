from django.shortcuts import redirect


class OwnershipRequiredMixin:
    """Making sure that only authors can update or delete instances"""

    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect("my-posts")
        return super(OwnershipRequiredMixin, self).dispatch(request, *args, **kwargs)


# class RedirectBackToPostAfterChangingMixin:
#     """Creating success url to return to post page"""
#     def get_success_url(self):
#         return reverse_lazy('post', kwargs={'pk': self.kwargs["post_id"]})
