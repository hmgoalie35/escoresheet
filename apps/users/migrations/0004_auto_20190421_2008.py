# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-21 20:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180527_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='permissions', to='contenttypes.ContentType', verbose_name='Content Type'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='permissions', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]