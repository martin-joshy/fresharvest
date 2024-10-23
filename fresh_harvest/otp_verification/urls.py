from django.urls import path

from . import views

urlpatterns = [
    path("phone-number-otp/", views.phone_number, name="phone-number-otp"),
    path("home", views.home, name="home"),
    path("phone-number/otp/<pk>/", views.otp_verify, name="otp"),
    path("resend-otp/<pk>/", views.resend_opt, name="resend-otp"),
]
