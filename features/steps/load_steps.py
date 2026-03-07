import requests
from behave import given
from os import getenv

BASE_URL = getenv("BASE_URL", "http://localhost:8080")

@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    # Reset database
    res = requests.get(f"{BASE_URL}/products")
    for product in res.json():
        requests.delete(f"{BASE_URL}/products/{product['id']}")

    # Load new data from Gherkin table
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'].lower() in ['true', '1', 'yes'],
            "category": row['category']
        }
        requests.post(f"{BASE_URL}/products", json=payload)