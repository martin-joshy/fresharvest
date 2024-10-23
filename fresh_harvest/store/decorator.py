from django.shortcuts import redirect

def authenticated_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('display-users')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func