# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-28 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0002_auto_20180219_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
    ]
