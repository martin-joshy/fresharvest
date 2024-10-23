from django import forms
from store.models import Category, Product, QuantityVariant, Seller
from image_cropping import ImageCropWidget
from cart.models import Order, Coupon
from django.urls import reverse_lazy
from offers.models import ProductOffer, CategoryOffer



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'title','is_active']


    name = forms.CharField(
        label='Category Name',
        max_length=30, 
        required=True, 
        help_text='Name of the category',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Category Name',
            'id': 'input-Category'
        })
    )

    title = forms.CharField(
        label='Category Info',
        max_length=50, 
        required=True, 
        help_text='Give a short title for the category',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Category Info',
            'id': 'input-Categoryinfo'
        })
    )


    is_active = forms.BooleanField(
        label='Visibility',
        required=False,
        help_text='Check if the product is active'
    )
    


# These include the form and custom templates related to the admin side product management

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description','quantity_type','price','image', 'is_active', 'current_stock']

    title = forms.CharField(
        label='Product Name',
        max_length=30, 
        required=True, 
        help_text='Optional.',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Product Name',
            'id': 'input-productname'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Category Menu',
        widget=forms.Select(attrs={
            'class': 'js-example-basic-single w-100 select2-hidden-accessible',
            'data-select2-id': 'select2-data-4-1nz0',
            'tabindex': '-1',
            'aria-hidden': 'true',
        })
    )


    price = forms.DecimalField(
    label='Price',
    max_digits=10,
    decimal_places=2,
    required=True,
    help_text='Enter the price of the product.',
    widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Price',
        'id': 'input-price'
    })
    )


    quantity_type = forms.ModelChoiceField(
        queryset=QuantityVariant.objects.all(),
        label='Quantity Type',
        empty_label='Quantity Type Menu',
        widget=forms.Select(attrs={
            'class': 'js-example-basic-single w-100 select2-hidden-accessible',
            'data-select2-id': 'select2-data-13-u367',
            'tabindex': '-1',
            'aria-hidden': 'true',
        })
    )

    description = forms.CharField(
        label='Description',
        max_length=300, 
        required=True, 
        help_text='Optional.',
        widget=forms.Textarea(attrs={
            'class': 'form-control ckeditor',  
            'placeholder': 'Description',
            'id': 'input-description'
        })
    )

    image = forms.ImageField(
        label='Image',
        widget=ImageCropWidget,
        required=True

    )
    is_active = forms.BooleanField(
        label='Visibility',
        required=False,
        help_text='Check if the product is active'
    )

    current_stock = forms.IntegerField(
        label='Current Stock',
        required=True,
        help_text='Enter the current stock of the product',
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Current Stock', 
            'id': 'input-current-stock'})
    )




# These include the form and custom templates related to the admin side product management

class SellerProductForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['product', 'stock', 'description', 'approved']

   
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Product',
        empty_label='Product Menu',
        widget=forms.Select(attrs={
            'class': 'js-example-basic-single w-100 select2-hidden-accessible',
            'data-select2-id': 'select2-data-4-1nz0',
            'tabindex': '-1',
            'aria-hidden': 'true',
        })
    )


    stock = forms.IntegerField(
    label='How Many',
    required=True,
    help_text='Enter how much you would like to add.',
    widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Price',
        'id': 'input-price'
    })
    )


    description = forms.CharField(
        label='Description',
        max_length=300, 
        required=True, 
        help_text='Optional.',
        widget=forms.Textarea(attrs={
            'class': 'form-control ckeditor',  
            'placeholder': 'Description',
            'id': 'input-description'
        })
    )

    approved = forms.BooleanField(
        label='Aprove',
        required=False,
        help_text='Approve the product'
    )

   


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']

        order_status = forms.ModelChoiceField(
            queryset=Order.objects.all(),
            label='Change the Order Status',
            empty_label='Options',
            widget=forms.Select(attrs={
                'class': 'form-control',
                'id': 'order_status'
                
            })
        )





class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'discount_price', 'minimum_amount','is_expired']

    coupon_code = forms.CharField(
        label='Coupon Code',
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Coupon Code',
            'id': 'coupon_code'
        })
    )


    discount_price = forms.DecimalField(
    label='Discount Price',
    max_digits=10,
    decimal_places=2,
    required=True,
    widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Discount Price',
        'id': 'discount_price'
    })
    )


    minimum_amount = forms.DecimalField(
    label='Minimum Amount',
    max_digits=10,
    decimal_places=2,
    required=True,
    widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Minimum Amount',
        'id': 'minimum_amount'
    })
    )


    is_expired = forms.BooleanField(
        label='Disable',
        required=False,
    )




class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['product', 'discount_percentage', 'start_date', 'end_date']


    product = forms.ModelChoiceField(
            queryset=Product.objects.all(),
            label='Select a Product',
            empty_label='Options',
            widget=forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Product',
                'id': 'product',
            })
        )


    discount_percentage = forms.DecimalField(
        label='Discount',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Discount Percentage',
            'id': 'discount_percentage'
    })
    )


    start_date = forms.DateTimeField(
        label='Start Date',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select Date',
            'id': 'start_date',
            'type': 'date',
    })
    )


    end_date = forms.DateTimeField(
        label='End Date',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select Date',
            'id': 'end_date',
            'type': 'date',
    })
    )




class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ['category', 'discount_percentage', 'start_date', 'end_date']


    category = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            label='Select a Category',
            empty_label='Options',
            widget=forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Category',
                'id': 'category',
            })
        )


    discount_percentage = forms.DecimalField(
        label='Discount',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Discount Percentage',
            'id': 'discount_percentage'
    })
    )


    start_date = forms.DateTimeField(
        label='Start Date',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select Date',
            'id': 'start_date',
            'type': 'date',
    })
    )


    end_date = forms.DateTimeField(
        label='End Date',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select Date',
            'id': 'end_date',
            'type': 'date',
    })
    )
    

