from django.urls import path, include
from . import views


urlpatterns = [
    path('cart-summary/', views.CartSummaryView.as_view(), name='cart-summary'),

    path('add/<int:product_id>/', views.cart_add, name= 'cart-add'),

    path('delete/<pk>', views.DeleteCartItem.as_view(), name= 'cart-delete'),

    path('update/<pk>/', views.UpdateCheckoutView.as_view(), name= 'cart-update'),

    path('checkout/', views.CheckoutView.as_view(), name= 'checkout'),



    # URLs related to coupon management
    path('cart-summary/apply-coupon/', views.CouponView.as_view(), name='apply-coupon'),

    path('cart-summary/delete-coupon/', views.CouponView.as_view(), name='delete-coupon'),




    path('success-page', views.success_page, name='success-page'),
  

]