# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-27 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divisions', '0002_division_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Slug'),
        ),
    ]
