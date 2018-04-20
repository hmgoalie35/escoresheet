# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-19 06:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.League')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='division',
            unique_together=set([('name', 'league'), ('slug', 'league')]),
        ),
    ]
