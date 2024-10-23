import factory 
from factory.django import DjangoModelFactory
from faker import Faker 

from .models import Client, Product, Sales 

fake = Faker() 

class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    name = factory.Faker('company')  # Generate company names
    country = factory.Faker('country')  # Generate countries


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')  # Generate random words as product names
    sku = factory.Faker('ean8')  # Generate fake EAN-8 barcodes


class SalesFactory(DjangoModelFactory):
    class Meta:
        model = Sales

    doc_date = factory.Faker('date_time_this_decade')
    client = factory.SubFactory(ClientFactory) 
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)

    # Update value based on quantity and price (after save)
    @factory.post_generation
    def calculate_value(self, create, extracted, **kwargs):
        if not create:
            # Simple calculation for demonstration. You may have more complex logic.
            self.value = self.quantity * self.price
            self.save()
