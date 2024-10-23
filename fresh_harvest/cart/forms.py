from user.forms import AddressForm


class NewCheckoutAddressForm(AddressForm):

    def __init__(self, *args, **kwargs):
        super(NewCheckoutAddressForm, self).__init__(*args, **kwargs)

        # Looping through the form fields and set required attribute to True
        for field_name, field in self.fields.items():
            field.required = False