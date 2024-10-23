from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from store.models import Profile
import random
from .helper import MessageHandler
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.urls import reverse
from django.views.decorators.cache import never_cache


# Function to send the opt to the user from the last update profile fields
def send_otp(user_profile):
    if user_profile.last_methodOtp  =="methodOtpWhatsapp":
        messagehandler=MessageHandler(user_profile.phone_number ,user_profile.otp).send_otp_via_whatsapp()
    else:
        messagehandler=MessageHandler(user_profile.phone_number ,user_profile.otp).send_otp_via_message()
    
    url = reverse('otp', kwargs={'pk': user_profile.pk })
    red=redirect(url)
    red.set_cookie("can_otp_enter",True,max_age=600)
    return red 


@never_cache
def phone_number(request):
    if request.method == 'POST':
        try:
            user_profile =Profile.objects.get(phone_number = str(request.POST['phone_number']))
            otp= str(random.randint(1000,9999))
            user_profile.otp = otp
            user_profile.last_methodOtp = request.POST['methodOtp']

            # Set the OTP expiry time to 10 minutes from now
            expiry_time = datetime.now() + timedelta(minutes=10)
            user_profile.otp_expiry = expiry_time

            user_profile.save()
            return send_otp(user_profile)

        except ObjectDoesNotExist as e:
            messages.error(request, 'No user with this number exists')

        except Exception as e:
            # Handle other exceptions (e.g., errors during OTP sending) and provide feedback to the user
            messages.error(request, 'An error occurred. Please try again later.')

    return render(request, 'phone-number.html')


@never_cache
def resend_opt(request, pk):
    user_profile =Profile.objects.get(pk=pk)
    otp= str(random.randint(1000,9999))
    user_profile.otp = otp

    # Set the OTP expiry time to 10 minutes from now
    expiry_time = datetime.now() + timedelta(minutes=10)
    user_profile.otp_expiry = expiry_time
    user_profile.save()
    return send_otp(user_profile)


@never_cache
def otp_verify(request,pk):
    profile=Profile.objects.get(pk=pk)   
    if request.method=="POST":
        user = User.objects.get(username = profile.user.username) 
        if request.COOKIES.get('can_otp_enter')!=None:
            if(profile.otp==request.POST.get('otp')):
                if user.is_active:
                    red=redirect('home')
                    red.set_cookie('verified',True)
                    login(request, user)
                    return red
                else:
                    messages.info(request, 'You have been temporary blocked')
            else: 
                messages.info(request, 'Wrong OTP. Please try again')       
    return render(request,"otp.html",{'id':pk , 'profile':profile})


def home(request):
    if request.COOKIES.get('verified') and request.COOKIES.get('verified')!=None:
        return redirect('store')
    else:
        return HttpResponse(" Not verified.")
