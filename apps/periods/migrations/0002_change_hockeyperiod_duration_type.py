# Generated by Django 2.2.17 on 2020-12-25 01:38

import django.core.validators
from django.db import migrations
import periods.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('periods', '0001_initial'),
    ]

    # period duration field has no data and postgres can't convert a postgres interval to integer so it's easier to just
    # remove the column and re-add it with the desired type
    operations = [
        migrations.RemoveField(
            model_name='hockeyperiod',
            name='duration',
        ),
        migrations.AddField(
            model_name='hockeyperiod',
            name='duration',
            field=periods.model_fields.PeriodDurationField(help_text='In minutes', null=True,
                                                           validators=[django.core.validators.MinValueValidator(1),
                                                                       django.core.validators.MaxValueValidator(60)]),
        ),
    ]
