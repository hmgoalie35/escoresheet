from django import forms

from escoresheet.utils import set_fields_disabled
from escoresheet.utils.formsets import BaseModelFormSet
from leagues.models import League
from .models import Referee


class RefereeForm(forms.ModelForm):
    prefix = 'referee'

    def __init__(self, *args, **kwargs):
        """
        Override the constructor to allow for custom kwargs to be passed to this form.

        :sport: The sport to filter teams by
        :read_only_fields: A list of fields that should be disabled in an HTML form. Note that using this will make
            django think the form 'has_changed' when it really hasn't.
        """
        sport = kwargs.pop('sport', None)
        read_only_fields = kwargs.pop('read_only_fields', None)
        super(RefereeForm, self).__init__(*args, **kwargs)
        if sport is not None:
            self.fields['league'].queryset = League.objects.filter(sport=sport)
        if read_only_fields is not None:
            set_fields_disabled(read_only_fields, self.fields)

    class Meta:
        model = Referee
        fields = ['league']


class RefereeModelFormSet(BaseModelFormSet):
    def clean(self):
        super(RefereeModelFormSet, self).clean()
        leagues_already_seen = []
        for form in self.forms:
            league = form.cleaned_data.get('league')
            if league is not None:
                if league.id in leagues_already_seen:
                    form.add_error('league',
                                   '{} has already been selected. '
                                   'Please choose another league or remove this form.'.format(league.full_name))
                else:
                    leagues_already_seen.append(league.id)
