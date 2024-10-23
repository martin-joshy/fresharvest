from django.shortcuts import render, redirect
from store.models import Product, Category, Seller
from .forms import CategoryForm, ProductForm, SellerProductForm, ChangeStatusForm, CouponForm, ProductOfferForm, CategoryOfferForm
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required    
from django.contrib.auth.models import User   
from store.forms import CreateUserForm, UpdateUserForm
from django.contrib import messages
from .decorator import authenticated_admin, admin_only, seller_only
from cart.models import Order, OrderItem, Coupon
from django.db.models import F, ExpressionWrapper, fields, Sum, Count, Q
from django.http import JsonResponse
from itertools import chain
from operator import attrgetter
from offers.models import ProductOffer, CategoryOffer

#admin category management

@admin_only
@login_required(login_url='login-admin')
@never_cache
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display-categories')
    else:
        form = CategoryForm()

    return render(request, 'create-category.html', {'form': form} )


@admin_only
@login_required(login_url='login-admin')
@never_cache
def display_categories(request):
    name = request.GET.get('name')
    all_categories = Category.objects.all().order_by('-id')
    if name:
        all_categories = all_categories.filter(name__icontains=name)
    context = {'all_categories': all_categories}
    return render(request, 'display-categories.html', context)


@admin_only
@login_required(login_url='login-admin')
@never_cache
def update_category(request, pk):
    instance_to_be_edited = Category.objects.get(pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('display-categories')
    else:
        form = CategoryForm(instance=instance_to_be_edited)

    context = {'form': form, 'category': instance_to_be_edited}
    return render(request, 'update-categories.html', context)


@admin_only
@login_required(login_url='login-admin')
@never_cache
def delete_category(request, pk):
    instance =Category.objects.get(pk=pk)
    instance.delete()
    return redirect('display-categories')



# views for the product management in admin

@admin_only
@login_required(login_url='login-admin')
@never_cache
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('display-products')
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'create-product.html', {'form': form} )


@admin_only
@login_required(login_url='login-admin')
@never_cache
def display_products(request):
    name = request.GET.get('name')
    all_products = Product.objects.all().order_by('-id')
    if name:
        all_products = all_products.filter(title__icontains=name)
    context = {'all_products': all_products}
    return render(request, 'display-products.html', context)


@admin_only
@login_required(login_url='login-admin')
@never_cache
def update_product(request, pk):
    instance_to_be_edited = Product.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('display-products')
    else:
        form = ProductForm(instance=instance_to_be_edited)
    context = {'form': form, 'product': instance_to_be_edited}
    return render(request, 'update-product.html', context)


@admin_only
@login_required(login_url='login-admin')
@never_cache
def delete_product(request, pk):
    instance =Product.objects.get(pk=pk)
    instance.delete()
    return redirect('display-products')




# views for the user management in admin

@admin_only
@login_required(login_url='login-admin')
@never_cache
def display_users(request):
    name = request.GET.get('name')
    users = User.objects.all().order_by('-id')
    if name:
        users = users.filter(username__icontains=name)
    context = {'users': users}
    return render(request, 'display-users.html', context)


@admin_only
@login_required(login_url='login-admin')
@never_cache
def delete_user(request, pk):
    instance =User.objects.get(pk=pk)
    instance.delete()
    return redirect('display-users')


@admin_only
@login_required(login_url='login-admin')
@never_cache
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display-users')
    else:
        form = CreateUserForm()  
    
    return render(request, 'create-users.html', {'form':form})


@admin_only
@login_required(login_url='login-admin')
@never_cache
def update_user(request, pk):
    instance_to_be_edited = User.objects.get(id=pk)

    form = UpdateUserForm(instance = instance_to_be_edited)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('display-users')

    context = {'form': form}
    return render(request, 'update-user.html', context)



@authenticated_admin
@never_cache
def login_admin(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(request, username= username, password= password)

        if user is not None :
            if user.groups.filter(name= 'admin').exists():
                login(request, user)
                return redirect('display-users')
            elif user.groups.filter(name= 'seller').exists():
                login(request, user)
                return redirect('display-seller-products') 
            else:
                logout(request)
                return redirect('login-admin')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context ={ }
    return render(request,'login.html', context)


def logout_admin(request):
    logout(request)
    return redirect('login-admin')




# view for the sellers 

@seller_only
@login_required(login_url='login-admin')
@never_cache
def add_products(request):
    if request.method == 'POST':
        # Set the user field with the currently authenticated user
        form = SellerProductForm(request.POST)
        if form.is_valid():
            seller_instance = form.save(commit=False)
            seller_instance.user = request.user  # Set the user field
            seller_instance.save()
            return redirect('display-seller-products')
        else:
            print(form.errors)
    else:
        form = SellerProductForm()
    return render(request, 'seller-product-add.html', {'form': form})


@seller_only
@login_required(login_url='login-admin')
@never_cache
def display_seller_products(request):
    name = request.GET.get('name')
    seller_product_instance = Seller.objects.filter(user = request.user)
    if name:
        seller_product_instance = seller_product_instance.filter(product__title__icontains=name)
    return render(request, 'display-seller-products.html', {'seller': seller_product_instance })



# This view is to get the all the seller product detail for approval
@admin_only
@login_required(login_url='login-admin')
@never_cache
def approve_product_display(request):
    name = request.GET.get('name')
    product_instance = Seller.objects.filter(approved = False)
    if name:
        product_instance = product_instance.filter(product__title__icontains=name)
    return render(request, 'approve-product-display.html', {'products': product_instance })


@admin_only
@login_required(login_url='login-admin')
@never_cache
def approve_product(request, pk):
    instance_to_be_edited = Seller.objects.get(id=pk)
    form = SellerProductForm(instance = instance_to_be_edited)
    if request.method == 'POST':
        # Set the user field with the currently authenticated user
        form = SellerProductForm(request.POST, instance=instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('approve-product-display')
        else:
            print(form.errors)
    context = {'form': form, 'sellers': instance_to_be_edited}
    return render(request, 'approve-product.html', context)




# View for Order Management
def display_order(request):
    all_order= Order.objects.all().order_by('-id')
    all_choices = Order.ORDER_STATUS_CHOICES
    unique_choices = [choice[0] for choice in all_choices]
    for order in all_order:
        order.total_price = order.calculate_total_price()
    return render(request,'orders/display-order.html', {'all_order': all_order, 'status_choices': unique_choices})


def display_order_detail(request,pk):
    order_instance = Order.objects.get(pk=pk)

    form = ChangeStatusForm(instance = order_instance)

    # Get order items with total prices annotated
    order_items = OrderItem.objects.filter(order=order_instance).annotate(
        total_price = ExpressionWrapper(
            F('qty') * F('price'),
            output_field= fields.DecimalField(max_digits=10, decimal_places=2)
        )
    )

    # calculate the grand total 
    grand_total = order_items.aggregate(grand_total = Sum('total_price'))['grand_total'] or 0

    # Get the count of total items in the order
    total_items_count = order_items.aggregate(total_items=Count('id'))['total_items']

    context = {'order_items':order_items, 
               'grand_total':grand_total, 
               'total_items_count': total_items_count,
               'order': order_instance,
               'form': form
               }
    return render(request, 'orders/display-order-detail.html', context)



# To Change the status of the Order
def change_status(request, pk):
    
    order_instance = Order.objects.get(pk=pk)
    form = ChangeStatusForm(instance = order_instance)
    if request.method == 'POST':
        # Set the user field with the currently authenticated user
        form = ChangeStatusForm(request.POST, instance=order_instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Order status updated successfully'}, status=200)
            
           


def display_coupon(request):
    name = request.GET.get('name')
    coupons_obj = Coupon.objects.all()
    if name:
        coupons_obj = coupons_obj.filter(coupon_code__icontains=name)

    coupons_obj = coupons_obj.order_by('-id')
    return render(request, 'coupon/display-coupon.html', {'coupons_obj': coupons_obj})



def create_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display-coupon')
    else:
        form = CouponForm()  
    
    return render(request, 'coupon/create-coupon.html', {'form':form})



def update_coupon(request, pk):
    instance_to_be_edited = Coupon.objects.get(id=pk)

    form = CouponForm(instance = instance_to_be_edited)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('display-coupon')

    context = {'form': form}
    return render(request, 'coupon/create-coupon.html', context)



def delete_coupon(request, pk):
    instance =Coupon.objects.get(pk=pk)
    instance.delete()
    return redirect('display-coupon')







def display_offers(request):
    name = request.GET.get('name')
    product_offers = ProductOffer.objects.all()
    category_offers = CategoryOffer.objects.all()
    all_offers = list(chain(product_offers, category_offers))
    if name:
        all_offers = [
                        offer 
                        for offer in all_offers 
                        if (offer.product.title and name.lower() in offer.product.title.lower()) 
                        or (offer.category.name and name.lower() in offer.category.name.lower())
                    ]

    sorted_offers = sorted(all_offers, key=lambda x: x.created_at, reverse=True)
   

    return render(request, 'offer/display-offers.html', {'sorted_offers': sorted_offers})



def create_offer(request):
    form_product = ProductOfferForm()
    form_category =  CategoryOfferForm()
    
    return render(request, 'offer/create-offer.html', {'form_product':form_product, 'form_category':form_category })



def create_product_offer(request):
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display-offers')



def create_category_offer(request):
    if request.method == 'POST':
        form =  CategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display-offers')




def update_offer(request, pk, offer_type):
    

    if offer_type == 'product':
        instance_to_be_edited = ProductOffer.objects.get(id=pk)
        form = ProductOfferForm(instance = instance_to_be_edited)
        if request.method == 'POST':
            form = ProductOfferForm(request.POST, instance=instance_to_be_edited)
            if form.is_valid():
                form.save()
                return redirect('display-offers')
    
    elif offer_type == 'category':
        instance_to_be_edited = CategoryOffer.objects.get(id=pk)
        form = CategoryOfferForm(instance = instance_to_be_edited)
        if request.method == 'POST':
            form = CategoryOfferForm(request.POST, instance=instance_to_be_edited)
            if form.is_valid():
                form.save()
                return redirect('display-offers')

    context = {'form': form, 'offer_type': offer_type}
    return render(request, 'offer/update-offer.html', context)




def delete_offer(request, pk, offer_type):

    if offer_type == 'product':
        instance =ProductOffer.objects.get(id=pk)
        instance.delete()
        return redirect('display-offers')
    
    elif offer_type == 'category':
        instance =CategoryOffer.objects.get(id=pk)
        instance.delete()
        return redirect('display-offers')


    


    





    











