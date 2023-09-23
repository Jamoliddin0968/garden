import random

from django.db import transaction
from faker import Faker

from .models import Product  # Replace 'myapp' with your app name

fake = Faker()

# Function to generate fake products


def generate_fake_products(num_products):
    fake_products = []

    for _ in range(num_products):
        name = fake.unique.name()  # Generate unique names
        measure = random.choice(
            ['kg', 'g', 'lb', 'oz', 'unit'])  # Random measure

        product = Product(name=name, measure=measure)
        fake_products.append(product)

    return fake_products

# Generate and save fake products


def save_fake_products(num_products):
    fake_products = generate_fake_products(num_products)

    with transaction.atomic():
        Product.objects.bulk_create(fake_products)


# Usage: Generate and save 10 fake products

save_fake_products(50)
