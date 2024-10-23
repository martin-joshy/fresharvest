from django import forms
from store.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


#creating custom templates for the forms
class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'input-username'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        help_text='Optional.',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'First Name',
            'id': 'input-firstname'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        help_text='Optional.',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Last Name', 
            'id': 'input-lastname'})
    )
    email = forms.EmailField(
        max_length=254, 
        required=True, 
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'id': 'input-email'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
            'id': 'input-telephone'}))
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password', 
            'id': 'input-password'})
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'id': 'input-confirm'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number']


    #below functions are to manually save the profile field as it is in different model
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = 'Phone Number'

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.save()

        # Create a related profile for the user with the phone number
        profile = Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])

        return user


class UpdateUserForm(forms.ModelForm):
    
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    
    class Meta:
        model = User
        fields = [ 'email', 'first_name', 'last_name', 'is_active']

