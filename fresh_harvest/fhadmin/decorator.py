from django.shortcuts import redirect

def authenticated_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name= 'admin').exists():
                return redirect('display-users')
            elif request.user.groups.filter(name= 'seller').exists(): 
                return redirect('display-seller-products')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login-admin')
    return wrapper_function


def seller_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.filter(name='seller').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login-admin')
    return wrapper_function