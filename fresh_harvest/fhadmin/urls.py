from django.urls import path
from .views import *

urlpatterns = [

    # testing
    # path('test/', test_admin, name= 'test-admin'),

    # URLs for the admin authentication
    path('login/', login_admin, name= 'login-admin'),
    path('logout/', logout_admin, name= 'logout-admin'),

    # URLs for the category management
    path('categories/', display_categories, name= 'display-categories'), 
    path('categories/create/', create_category, name= 'create-category'), 
    path('categories/update/<pk>', update_category, name= 'update-category'),
    path('categories/delete/<pk>', delete_category, name= 'delete-category'),
    # path('search/', search_category, name= 'search-category'), # check why this view did not work before

    # URLs for the Product management
    path('products/', display_products, name= 'display-products'), 
    path('products/create/', create_product, name= 'create-product'), 
    path('products/update/<pk>', update_product, name= 'update-product'),
    path('products/delete/<pk>', delete_product, name= 'delete-product'), 

    # URLs for the User Management
    path('users/', display_users, name= 'display-users'), 
    path('users/create/', create_user, name= 'create-user'), 
    path('users/delete/<pk>', delete_user, name= 'delete-user'), 
    path('users/update/<pk>', update_user, name= 'update-user'),

    # URLs for the Admin to manage seller requests
    path('product/approve-display', approve_product_display, name= 'approve-product-display'), 
    path('product/approve/<pk>', approve_product, name= 'approve-product'),


    #URLs for Seller 
    path('product/add', add_products , name= 'add-products'), 
    path('product/display', display_seller_products , name= 'display-seller-products'), 


    #URLs for Order Management
    path('order/display', display_order, name= 'display-order'), 
    path('order/display/detail/<pk>', display_order_detail, name= 'display-order-detail'),
    path('order/<int:pk>', change_status, name= 'change-status'),   


    # URLs for Coupon Management
    path('display-coupon', display_coupon, name= 'display-coupon'),
    path('create-coupon', create_coupon, name= 'create-coupon'),
    path('update-coupon/<int:pk>', update_coupon, name= 'update-coupon'), 
    path('delete-coupon/<int:pk>', delete_coupon, name= 'delete-coupon'),     


    # URLs for Offer Management
    path('display-offers', display_offers, name= 'display-offers'),
    path('create-offer', create_offer, name= 'create-offer'),
    path('create-product-offer', create_product_offer, name= 'create-product-offer'),
    path('create-category-offer', create_category_offer, name= 'create-category-offer'),
    path('update-offer/<int:pk>/<str:offer_type>', update_offer, name= 'update-offer'), 
    path('delete-offer/<int:pk>/<str:offer_type>', delete_offer, name= 'delete-offer'),    





    
]

