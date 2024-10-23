from django.shortcuts import render, redirect
from .models import Category, Product
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.core.exceptions import ObjectDoesNotExist
from .decorator import authenticated_user
from django.db import IntegrityError



@never_cache
@login_required(login_url='login')
def store(request):
    all_products = Product.objects.filter(current_stock__gt=0, is_active=True) 
    
    context = {'all_products': all_products }
    return render(request, 'store/store.html', context)


# Available throughout the project 
def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories':all_categories}


def user_groups(request):
    groups = []
    user = request.user
    if request.user.is_authenticated:
        groups = request.user.groups.values_list('name', flat=True)

    return {'user_groups': groups}

@never_cache
@login_required(login_url='login')
def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {'product':product}
    return render(request, 'store/product-info.html',context)

@never_cache
@login_required(login_url='login')
def list_category(request, category_slug= None):
    category = get_object_or_404(Category, slug= category_slug)
    all_products = Product.objects.filter(category= category)
    return render(request, 'store/list-category.html', {'category': category, 'all_products': all_products})
  


#URLs to authenticate and register the user 


@authenticated_user
@never_cache
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if the user exists
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = None
        if user is not None and user.is_active:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('store')
            else:
                messages.info(request, 'Username or password is incorrect')
        elif user is not None:
            messages.info(request, 'You have been temporarily blocked')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'store/user-login.html')



def logout_user(request):
    logout(request)
    return redirect('login')


@never_cache
def signup_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
            except IntegrityError as e:
                if 'phone_number' in str(e):
                    form.add_error('phone_number', 'Phone number is already in use.')
                else:
                    # Handle other IntegrityErrors or re-raise if it's not related to phone_number
                    raise
    context = {'form': form}
    return render(request, 'store/signup-user.html', context)




