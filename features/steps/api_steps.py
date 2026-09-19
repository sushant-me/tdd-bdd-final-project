"""Step definitions for the API-level acceptance tests (features/api.feature)."""
import requests
from behave import then, when

# Generous but finite: a hung service should fail the step, not the job.
TIMEOUT = 10


@when('I request the list of all products')
def step_impl(context):
    context.response = requests.get(f"{context.base_url}/products", timeout=TIMEOUT)


@when('I request the products with name "{name}"')
def step_impl(context, name):
    context.response = requests.get(
        f"{context.base_url}/products", params={"name": name}, timeout=TIMEOUT
    )


@when('I request the products in category "{category}"')
def step_impl(context, category):
    context.response = requests.get(
        f"{context.base_url}/products", params={"category": category}, timeout=TIMEOUT
    )


@when('I request the products that are available')
def step_impl(context):
    context.response = requests.get(
        f"{context.base_url}/products", params={"available": "true"}, timeout=TIMEOUT
    )


@when('I request the product named "{name}" by id')
def step_impl(context, name):
    listing = requests.get(
        f"{context.base_url}/products", params={"name": name}, timeout=TIMEOUT
    )
    assert listing.status_code == 200, listing.text
    matches = listing.json()
    assert matches, f"no product named {name!r} was loaded, cannot retrieve it"
    context.response = requests.get(
        f"{context.base_url}/products/{matches[0]['id']}", timeout=TIMEOUT
    )


@then('the response status should be {status:d}')
def step_impl(context, status):
    assert context.response.status_code == status, (
        f"expected HTTP {status} but got {context.response.status_code}: "
        f"{context.response.text}"
    )


@then('the response should contain {count:d} products')
def step_impl(context, count):
    payload = context.response.json()
    assert isinstance(payload, list), f"expected a list of products, got {payload!r}"
    assert len(payload) == count, (
        f"expected {count} product(s) but got {len(payload)}: {payload}"
    )


@then('the response should contain a product named "{name}"')
def step_impl(context, name):
    payload = context.response.json()
    products = payload if isinstance(payload, list) else [payload]
    assert any(p.get("name") == name for p in products), (
        f"no product named {name!r} in {payload}"
    )
