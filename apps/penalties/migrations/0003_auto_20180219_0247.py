# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-19 02:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('penalties', '0002_auto_20171209_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hockeypenalty',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created'),
        ),
    ]
