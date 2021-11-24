from django.shortcuts import redirect


class OwnershipRequiredMixin:
    """Making sure that only authors can update or delete instances"""

    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect("my-posts")
        return super(OwnershipRequiredMixin, self).dispatch(request, *args, **kwargs)
