# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-07 20:26
from __future__ import unicode_literals

from django.db import migrations


def fix_phone_number(apps, schema_editor):
    Location = apps.get_model('locations', 'Location')
    locations = Location.objects.all()
    for location in locations:
        location.phone_number = location.phone_number.replace('-', ' ', 1)
        location.save()


class Migration(migrations.Migration):
    dependencies = [
        ('locations', '0004_auto_20171225_0337'),
    ]

    operations = [
        migrations.RunPython(fix_phone_number, migrations.RunPython.noop)
    ]