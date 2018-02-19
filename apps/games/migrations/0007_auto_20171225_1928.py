# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-25 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20171222_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hockeygame',
            name='timezone',
            field=models.CharField(choices=[('US/Alaska', 'US/Alaska'), ('US/Arizona', 'US/Arizona'), ('US/Central', 'US/Central'), ('US/Eastern', 'US/Eastern'), ('US/Hawaii', 'US/Hawaii'), ('US/Mountain', 'US/Mountain'), ('US/Pacific', 'US/Pacific'), ('UTC', 'UTC')], max_length=128, verbose_name='Timezone'),
        ),
    ]