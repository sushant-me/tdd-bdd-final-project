from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@when('I set the "{field}" to "{value}"')
def step_impl(context, field, value):
    element_id = field.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(value)

@when('I click the "{button_text}" button')
def step_impl(context, button_text):
    element_id = button_text.lower().replace(' ', '-') + "-btn"
    context.driver.find_element(By.ID, element_id).click()

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element((By.ID, 'flash_message'), message)
    )
    assert found