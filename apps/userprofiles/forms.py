import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from django import forms
from django.utils.translation import ugettext_lazy as _

from escoresheet.utils import SelectDateMonthDayYearInitiallyBlankWidget
from .models import UserProfile

YEAR_DIFFERENCE = 20
MAX_AGE = 100


class CreateUserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Field('gender'),
                # This makes the birthday select tags inline
                Field('birthday', wrapper_class='form-inline'),
                Field('height'),
                Field('weight'),
                Field('language'),
                Field('timezone'),
                HTML('<br>'),
                Div(Submit('create_userprofile_btn', 'Create profile and continue', css_class='btn btn-success'),
                    css_class='text-center'),
                HTML('<br>'),
        )

    current_year = datetime.datetime.today().year
    year_range = range(current_year - MAX_AGE, current_year + 1)
    birthday = forms.DateField(
            widget=SelectDateMonthDayYearInitiallyBlankWidget(years=year_range))

    class Meta:
        model = UserProfile
        fields = ['gender', 'birthday', 'height', 'weight', 'language', 'timezone']
        labels = {
            'weight': _('Weight (in lbs)')
        }


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['height', 'weight', 'language', 'timezone']
        labels = {
            'weight': _('Weight (in lbs)')
        }


class UserProfileAdminForm(forms.ModelForm):
    current_year = datetime.datetime.today().year
    year_range = range(current_year - MAX_AGE, current_year + 1)
    birthday = forms.DateField(
            widget=SelectDateMonthDayYearInitiallyBlankWidget(years=year_range))

    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'birthday', 'height', 'weight', 'language', 'timezone']
        labels = {
            'weight': _('Weight (in lbs)'),
        }
