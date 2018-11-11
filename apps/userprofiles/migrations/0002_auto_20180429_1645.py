# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-29 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
    ]
