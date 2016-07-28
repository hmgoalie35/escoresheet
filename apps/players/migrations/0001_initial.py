# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 02:16
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sports', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HockeyPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jersey_number', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)], verbose_name='Jersey Number')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('position', models.CharField(choices=[('C', 'C'), ('LW', 'LW'), ('RW', 'RW'), ('LD', 'LD'), ('RD', 'RD'), ('G', 'G')], max_length=255, verbose_name='Position')),
                ('handedness', models.CharField(choices=[('Left', 'Left'), ('Right', 'Right')], max_length=255, verbose_name='Shoots')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.Sport')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='hockeyplayer',
            unique_together=set([('user', 'team'), ('user', 'sport')]),
        ),
    ]
