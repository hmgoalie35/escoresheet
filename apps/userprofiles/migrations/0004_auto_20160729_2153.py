# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-29 21:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0003_rolesmask_is_complete'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rolesmask',
            options={'ordering': ['user']},
        ),
    ]
