import re

from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from localflavor.us import models as us_models
from localflavor.us.us_states import US_STATES

from ayrabo.utils.model_fields import WebsiteField
from common.models import TimestampedModel


PHONE_NUMBER_REGEX = re.compile(r'^\(?[2-9]\d{2}\)? \d{3}-\d{4}$')


class Location(TimestampedModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    street = models.CharField(max_length=255, verbose_name='Street')
    street_number = models.CharField(max_length=255, verbose_name='Street Number')
    city = models.CharField(max_length=255, verbose_name='City')
    # Didn't use localflavor's USStateField because only wanted the 50 U.S. states
    state = models.CharField(max_length=2, choices=US_STATES, verbose_name='State')
    zip_code = us_models.USZipCodeField(verbose_name='Zip Code')
    phone_number = models.CharField(
        max_length=255,
        verbose_name='Phone Number',
        validators=[RegexValidator(regex=PHONE_NUMBER_REGEX, message='Enter a valid phone number.', code='invalid')]
    )
    website = WebsiteField()

    def clean(self):
        # Don't call .save here for 2 reasons. 1. In the admin pressing save w/o entering anything will result in a
        # blank slug because this doesn't check if self.name exists. 2. validate_unique runs after clean, so don't want
        # to save things before all validation is finished.
        self.slug = slugify(self.name)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamLocation(TimestampedModel):
    """
    Used as a through model for a Team's relation to Location (m2m)
    """
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    primary = models.BooleanField(default=False, verbose_name='Primary Location')

    class Meta:
        unique_together = (
            ('team', 'location')
        )

    def __str__(self):
        return '{}: {}'.format(self.team.name, self.location.name)
