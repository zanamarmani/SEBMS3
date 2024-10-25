from django.http import HttpResponseForbidden
from django.shortcuts import redirect
def consumer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_consumer:
            return view_func(request, *args, **kwargs)
        return redirect("login")
    return _wrapped_view
