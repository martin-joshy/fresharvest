from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Address, WishList, WishListItem, WalletTransaction
from cart.models import Order, OrderItem
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.db.models import F, ExpressionWrapper, fields, Sum
from django.http import HttpResponse
from store.models import Product
from cart.models import Cart, CartItem
import json
from django.http import JsonResponse






# Display the user details

def test(request):
    return render(request, 'account/user-account-edit.html')


def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdationForm(request.POST, instance=request.user)
        profile_form = ProfileUpdationForm(request.POST, instance=request.user.profile)   
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('store')  
    else:
        user_form = UserUpdationForm(instance=request.user)
        profile_form = ProfileUpdationForm(instance=request.user.profile)
    return render(request, 'account/user-account-edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



# View for related to address 

# To display the user address

def display_address(request):
    all_address = Address.objects.filter(user = request.user)
    return render(request, 'account/display-address.html', {'all_address': all_address} )



# To add a new address

def add_address(request):
    if request.method == 'POST':
        # Set the user field with the currently authenticated user
        form = AddressForm(request.POST)
        if form.is_valid():
            address_instance = form.save(commit=False)
            address_instance.user = request.user  # Set the user field
            address_instance.save()
            redirect_to = request.POST.get('next', 'display-address') # To redirect using the 
            if redirect_to == 'checkout':
                messages.info(request, "New address has been added, if you wish to continue with please select and press continue")
            return redirect(redirect_to)                              # value of next
        else:
            print(form.errors)
    else:
        form = AddressForm()
    return render(request, 'account/add-address.html', {'form': form} )



# To update an existing address

def edit_address(request, pk):
    instance_to_be_edited = Address.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('display-address')
    else:
        form = AddressForm(instance=instance_to_be_edited)
    return render(request, 'account/edit-address.html', {'form': form})


def delete_address(request, pk):
    instance =Address.objects.get(pk=pk)
    instance.delete()
    return redirect('display-address')



# view to modify the behaviour of the build in class for password reset

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "password-reset.html"
    success_url = reverse_lazy('login')
    form_class=CustomPasswordResetForm

    def form_valid(self, form):
        messages.success(self.request, 'Password reset email has been sent. Please check your inbox.')
        return super().form_valid(form)



# view to redirect the user to user home page and display message after successful pasword reset
    
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name="password-reset-form.html"
    post_reset_login = True
    success_url = reverse_lazy('store')
    form_class= CustomSetPasswordForm

    def form_valid(self, form):
        messages.success(self.request, 'Password has been successfully reset.')
        return super().form_valid(form)
    



# View related to Order History 

def display_order_history(request):
    all_orders= Order.objects.filter(user=request.user).order_by('-pk')

    for order in all_orders:
        order.total_price = order.calculate_total_price()
    

    return render (request, 'history/display-order-history.html', {'all_orders':all_orders})



# view for detailed view of individual items in an order

def detailed_order_history(request, pk):
    order_instance = Order.objects.get(pk=pk)
    

    order_items = OrderItem.objects.filter(order=order_instance).annotate(
            total_price=ExpressionWrapper(
                F('qty') * F('price'),
                output_field=fields.DecimalField(max_digits=10, decimal_places=2)
            ),
            total_discount=ExpressionWrapper(
                F('qty') * F('discount'),
                output_field=fields.DecimalField(max_digits=10, decimal_places=2)
            )
        )   
    

    total_order_amount_before_discount = order_items.aggregate(
        total_order_amount_before_discount = Sum('total_price'))['total_order_amount_before_discount'] or 0

    total_order_discount = abs(order_items.aggregate(total_order_discount = Sum('total_discount'))['total_order_discount'] or 0)

    coupon_discount = order_instance.coupon_discount

    total_order_amount_after_all_discount = total_order_amount_before_discount - total_order_discount - coupon_discount

    context = {
        'total_order_amount_before_discount': total_order_amount_before_discount,
        'total_order_discount': total_order_discount,
        'total_order_amount_after_all_discount': int(total_order_amount_after_all_discount),
        'coupon_discount': coupon_discount,
        'order_items':order_items,
        'order_instance': order_instance,
        'pk':pk

    }


    return render (request, 'history/detailed-order-history.html', context)



# view to cancel any existing order

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Check if the order is already canceled
    if order.canceled:
        messages.warning(request, "This order is already canceled.")
    else:
        order.order_status = 'Canceled'
        if order.payment_method == 'COD':
            messages.success(request, "Your order has been canceled ")
        else:
            wallet_refund = WalletTransaction.objects.create(
                title = 'Cancellation refund',
                description = f'Amount refunded of the Order - {str(order.uuid)[:6]} placed on {order.order_date.strftime("%Y-%m-%d")}',
                amount = order.grand_total(),
                user = request.user
                
            )
            messages.success(request, "Your order has been canceled and the amount has been refunded to your wallet ")

    order.canceled = True
    order.save()
    return redirect('display-order-history')




# class view which validates the form field



def firstname_validation(request):
    if not request.POST["first_name"]:
        return HttpResponse('Please fill out this field')
    else:
        return HttpResponse("")
    

def lastname_validation(request):
    if not request.POST["last_name"]:
        return HttpResponse('Please fill out this field')
    else:
        return HttpResponse("")
    

def address_validation(request):
    if not request.POST["address_line_1"]:
        return HttpResponse('Please fill out this field')
    else:
        return HttpResponse("")


def city_validation(request):  
    if not request.POST["city"]:
        return HttpResponse('Please fill out this field')
    else:
        return HttpResponse("")
    

def post_code(request):  

    post_code = request.POST.get("post_code")
    if not post_code:
        return HttpResponse('Please fill out this field')
    elif len(post_code) != 6:
        return HttpResponse('Please enter a valid number')
    else:
        return HttpResponse("")
    

def phone_number(request):  
    phone_number_value = request.POST.get("phone_number")
    if not phone_number_value:
        return HttpResponse('Please fill out this field')
    elif len(phone_number_value) != 10:
        return HttpResponse('Please enter a valid number')
    else:
        return HttpResponse("")
    

def region_validation(request):
    phone_number_value = request.POST.get("region")
    if not phone_number_value:
        return HttpResponse('Please select one')
    else:
        return HttpResponse("")


    


# View for Wish list


def wishlist_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    wishlist_item, created = WishListItem.objects.get_or_create(
        wishlist=wishlist, product=product)
   
    if not created:
        messages.warning(request, "The Products exist in the WishList")
    else:
        messages.success(request, "The item has been added to the WishList")
            
    return redirect(request.META['HTTP_REFERER'])


def wishlist_display(request):
    wishlist= WishList.objects.filter(user = request.user).first()
    wishlist_items = WishListItem.objects.filter(wishlist = wishlist)
    context = {'wishlist_items':wishlist_items}
    return render(request, 'account/wish-list.html', context)


def remove_from_wishlist(request, pk):
    to_remove = WishListItem.objects.get(pk=pk)
    to_remove.delete()

    return redirect('wish-list')



def cart_add_from_wishlist(request, pk):
    wishlist_item = get_object_or_404(WishListItem, pk =pk)
    product = wishlist_item.product
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = 1
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    
    if not created:
        messages.warning(request, "The Products exist in the cart")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        wishlist_item.delete()

        messages.success(request, "The item has been added to the cart")

    return redirect(request.META['HTTP_REFERER'])




def display_wallet(request):
    
    current_user = request.user
    user_wallet_transaction = WalletTransaction.objects.filter(user=current_user).order_by('-transaction_date')
    total_balance = WalletTransaction.objects.filter(user=current_user).aggregate(total_balance=Sum('amount'))['total_balance'] or 0
    return render(request, 'wallet/display-wallet.html', {'user_wallet_transaction':user_wallet_transaction, 'total_balance':total_balance})



def topup_wallet(request):

    current_user = request.user
    total_balance = WalletTransaction.objects.filter(user=current_user).aggregate(total_balance=Sum('amount'))['total_balance'] or 0
    return render(request, 'wallet/topup-wallet.html', {'total_balance':total_balance})



def topup_wallet_success(request, amount):

    title = "Wallet Topup"
    user = request.user
    description = f"Topup made to the account of {user.first_name} {user.last_name}"
    amount = float(amount)
    

    wallet_object = WalletTransaction.objects.create(
        title=title,
        description=description,
        amount=amount,
        user=user   
    )

    messages.success(request, "The payment was made successfully")
    return redirect('display-wallet')



def fetch_external_html(request):
 
    context = {
       
    }
    return render(request, 'invoice.html', context) 


def compelete_failed_order(request, pk):
    order_instance = Order.objects.get(pk=pk)
    amount = order_instance.grand_total()
    return render(request, 'history/compelete-failed-order.html', {'amount':amount, 'pk':pk})



def pay_failed_order(request):
     
     if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')
            order_id = data.get('orderId')

            if status == 'Completed':
                messages.success("The payment was successful")
            if status == 'Pending':
                messages.warning("The payment was is yet to be confirmed, We will notify you the status..")
            if status == 'Failed':
                messages.error("The payment was Unsuccessful... Please try again")


            order_instance = Order.objects.get(pk=order_id)
            order_instance.payment_status = status
            order_instance.save()

            return redirect('detailed-order-history', kwargs={'pk': order_id})

        
        except json.JSONDecodeError:
            messages.error("Something went wrong. Please try again...")
            return redirect(request.META.get('HTTP_REFERER', '/'))
            





