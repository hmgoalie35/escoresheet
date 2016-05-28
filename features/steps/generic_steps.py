from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.db.models import Q
from behave import *
import re


def find_element(context, element_to_find):
    """
    Given an element's id, class name, name, etc. try to find that element on the page
    :param context: The testing context (contains the driver, django test runner, etc)
    :param element_to_find: The id, name, etc of the element to be located
    :return: A selenium WebElement. API available at https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement
    """
    methods_to_find_by = [By.ID, By.CLASS_NAME, By.CSS_SELECTOR, By.LINK_TEXT, By.NAME, By.PARTIAL_LINK_TEXT,
                          By.TAG_NAME, By.XPATH]
    for method in methods_to_find_by:
        try:
            element = context.driver.find_element(method, element_to_find)
            return element
        except NoSuchElementException:
            pass
    raise NoSuchElementException('{element} does not exist on the page'.format(element=element_to_find))


@given('I am on the "(?P<url>.*)" page')
def step_impl(context, url):
    context.driver.get(context.get_url(url))


@step('I go to the "(?P<url>[^"]*)" page')
def step_impl(context, url):
    step = 'given I am on the "{url}" page\n'.format(url=url)
    context.execute_steps(step)


@step('I fill in "(?P<element>.*)" with "(?P<value>.*)"')
def step_impl(context, element, value):
    the_element = find_element(context, element)
    the_element.send_keys(value)


@step('I press "(?P<element>.*)"')
def step_impl(context, element):
    the_element = find_element(context, element)
    the_element.click()


@step('I should be on the "(?P<url>.*)" page')
def step_impl(context, url):
    current_url = context.driver.current_url
    # Check for query params and discard if exist
    if '?' in context.driver.current_url:
        current_url = current_url.split('?')[0]
    context.test.assertEqual(current_url, context.get_url(url))


@step('I should see "(?P<text>.*)"')
def step_impl(context, text):
    context.test.assertIn(text, str(context.driver.page_source))


@step('A user account should exist for "(?P<username_or_email>.*)"')
def step_impl(context, username_or_email):
    context.test.assertIsInstance(User.objects.get(Q(username=username_or_email) | Q(email=username_or_email)), User)


@step('"(?P<text>.*)" should show up (?P<num>.*) times?')
def step_impl(context, text, num):
    # findall returns a list of all matches
    num_matches = len(re.findall(text, context.driver.page_source))
    context.test.assertEqual(int(num), num_matches)
