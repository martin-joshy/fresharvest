from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #URLs to list products on the user side
    path('store/', views.store, name='store'),
    path('product/<slug:slug>/', views.product_info, name='product-info'),
    path('search/<slug:category_slug>/', views.list_category, name='list_category'),

    #URLs to authenticate and register the user 
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),


]