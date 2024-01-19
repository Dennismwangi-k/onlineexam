from django.http import HttpResponse

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            elif request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to access this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page!!')
    return wrapper_func
