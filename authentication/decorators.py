from functools import wraps
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    allowed = {str(role).lower() for role in allowed_roles}

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            role = getattr(getattr(request.user, "profile", None), "role", None)
            if role is None or str(role).lower() not in allowed:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
