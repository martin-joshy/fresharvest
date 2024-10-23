
from django import forms
from store.models import User, Profile
from .models import Address, Region
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.validators import MaxLengthValidator
from django.urls import reverse_lazy


# For updating the User profile

class UserUpdationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }




# To update the user address
        
class AddressForm(forms.ModelForm):

    post_code = forms.CharField(
        label='Post Code', 
        max_length = 6,
        min_length = 6,
       
        widget=forms.TextInput(attrs={
            'class': 'numeric-field form-control',
            'placeholder': '*Post Code',
            'hx-post': reverse_lazy("post-code"),
            'hx-target': '#post_codeValidationError',
            'hx-trigger': 'blur',
            'required': True
        })
    )


    phone_number = forms.CharField(
        label='Phone Number',
        max_length = 10,
        min_length = 10,
        
        widget=forms.TextInput(attrs={
            
            'class': 'numeric-field form-control',
            'placeholder': '*Phone Number',
            'hx-post': reverse_lazy("phone-number"),
            'hx-target': '#phone_numberValidationError',
            'hx-trigger': 'blur',
            'required': True
        })
        
    )



    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label='*Region Menu',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'hx-post': reverse_lazy("region-validation"),
            'hx-target': '#regionValidationError',
            'hx-trigger': 'blur',
            'required': True,
        }),
    )

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'address_line_1', 'address_line_2',
                  'city', 'post_code', 'region', 'default_address', 'phone_number']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 
                                                 'placeholder': '*First Name',
                                                 'hx-post': reverse_lazy("first-name-validation"),
                                                 'hx-target': '#first_nameValidationError',
                                                 'hx-trigger': 'blur',
                                                 'required': True
                                                 }),

            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*Last Name',
                                                 'hx-post': reverse_lazy("last-name-validation"),
                                                 'hx-target': '#last_nameValidationError',
                                                 'hx-trigger': 'blur',
                                                 'required': True
                                                }),

            'address_line_1': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': '*Address Line 1',
                                                     'hx-post': reverse_lazy("address-validation"),
                                                     'hx-target': '#address_line_1ValidationError',
                                                     'hx-trigger': 'blur',
                                                     'required': True
                                                    }),

            'address_line_2': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Address Line 2'
                                                    }),

            'city': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '*City',
                                            'hx-post': reverse_lazy("city-validation"),
                                            'hx-target': '#cityValidationError',
                                            'hx-trigger': 'blur',
                                            'required': True
                                          }),

            
            'default_address': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

     
        }


       


        

        
        
    # def clean_default_address(self):
    #     default_address = self.cleaned_data['default_address']
    #     user = self.instance.user

    #     # If trying to set as default, update other addresses
    #     if default_address:
    #         Address.objects.filter(user=user).update(default_address=False)

    #     return default_address
 

# Forms for Password change
        
# overriding the PasswordResetForm widget for custom styling
           
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your email Address'}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your new Password'}),
        label='New password'
    )
    new_password2 = forms.CharField(
        label='Confirm your password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your new Password'}),
    )

 





          

   

