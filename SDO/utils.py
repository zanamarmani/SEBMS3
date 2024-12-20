from django.http import HttpResponseForbidden
from django.shortcuts import redirect
def sdo_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print(f"User in utils Authenticated: {request.user.is_authenticated}, Is SDO: {getattr(request.user, 'is_sdo', False)}")
        if request.user.is_authenticated and request.user.is_sdo:
            return view_func(request, *args, **kwargs)
        return redirect("login")
    return _wrapped_view
