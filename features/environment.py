from behave import use_step_matcher
from django.contrib.sites.models import Site
from selenium import webdriver

use_step_matcher('re')


def before_all(context):
    context.driver = webdriver.PhantomJS()
    # context.driver = webdriver.Firefox()
    # context.driver = webdriver.Chrome(executable_path=os.path.join(settings.BASE_DIR, 'selenium_drivers', 'chromedriver-linux'))
    context.driver.maximize_window()


def after_all(context):
    context.driver.quit()


def before_scenario(context, scenario):
    site = Site.objects.get_current()
    site.name = 'localhost'
    site.domain = context.get_url().split('http://')[1]
    site.save()
