from django.urls import path, include
from .import views

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy





urlpatterns = [


    # password management views

    path('otp-verification/', include('otp_verification.urls')),

    # 1. Summit our email from
    path('reset-password', views.CustomPasswordResetView.as_view() ,name='reset_password'),

    # 2. Pasword resent link, after the password is set, the user is redirected to the home page 
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),                                                                        



    # User account management view
    
    # 1. To update the profile 
    path('update-profile', views.update_profile, name= 'update-profile'),

    #2. To view address book
    #2.1 To see all the address record 
    path('display-address', views.display_address, name = 'display-address'),

    #2.2 To edit perticular address record
    path('edit-address/<int:pk>/', views.edit_address, name = 'edit-address'),

    #2.3 To delete perticular address record
    path('delete-address/<int:pk>/', views.delete_address, name = 'delete-address'),

    #2.4 To add an address
    path('add-address', views.add_address, name = 'add-address'),




    # 3.Order History Views
    # 3.1 Order History
    path('display-order-history', views.display_order_history, name = 'display-order-history'),

    # 3.2 Detailed Order History
    path('detailed-order-history/<int:pk>/', views.detailed_order_history, name = 'detailed-order-history'),

    #3.3 Cancel order
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel-order'),

    path('compelete-failed-order/<int:pk>/', views.compelete_failed_order, name= 'compelete-failed-order'), 

    path('pay-failed-order/', views.pay_failed_order, name= 'pay-failed-order'), 




    #4.1 URLs for validations
    path('first-name-validation/', views.firstname_validation, name= 'first-name-validation'),

    path('last-name-validation/', views.lastname_validation, name= 'last-name-validation'), 

    path('address-validation/', views.address_validation, name= 'address-validation'), 

    path('city-validation/', views.city_validation, name= 'city-validation'),

    path('post-code/', views.post_code, name= 'post-code'),
        
    path('phone-number/', views.post_code, name= 'phone-number'),     

    path('region-validation/', views.region_validation, name= 'region-validation'),  


    # Wish List 
    path('wish-list', views.wishlist_display, name= 'wish-list'), 

    path('wishlist-add/<int:product_id>/', views.wishlist_add, name= 'wishlist-add'), 

    path('remove-from-wishlist/<int:pk>/', views.remove_from_wishlist, name= 'remove-from-wishlist'), 

    path('cart-add-from-wishlist/<int:pk>/', views.cart_add_from_wishlist, name= 'cart-add-from-wishlist'), 


    # wallet 
    path('display-wallet', views.display_wallet, name= 'display-wallet'),

    path('topup-wallet', views.topup_wallet, name= 'topup-wallet'), 

    path('topup-wallet-success/<str:amount>/', views.topup_wallet_success, name= 'topup-wallet-success'),



    # URL for pdf 
    path('get-external-html/', views.fetch_external_html, name='get_external_html'),



    



    





]
