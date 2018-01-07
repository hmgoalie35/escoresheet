import random

import factory
from factory import post_generation, Faker, django
from localflavor.us.us_states import US_STATES

from locations.models import Location

random.seed(None)


def generate_num(low, high, count):
    return ''.join([str(random.randint(low, high)) for _ in range(count)])


def generate_phone_number():
    left = generate_num(2, 9, 1) + generate_num(0, 9, 2)
    middle = generate_num(0, 9, 3)
    right = generate_num(0, 9, 4)
    return '({}) {}-{}'.format(left, middle, right)


class LocationFactory(django.DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.sequence(lambda x: 'Location {}'.format(x))
    # slug is autogenerated via overridden .clean() method on the model
    street = Faker('street_name')
    street_number = Faker('building_number')
    city = Faker('city')
    state = Faker('random_element', elements=[state[0] for state in US_STATES])
    zip_code = Faker('zipcode')
    phone_number = factory.LazyFunction(generate_phone_number)
    website = Faker('url')

    @post_generation
    def full_clean(self, obj, extracted, **kwargs):
        self.full_clean(exclude=['slug'])
