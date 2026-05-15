from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps


def rol_requerido(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.rol not in roles:
                raise PermissionDenied("No tienes permiso para acceder a esta página")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
