# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-02 20:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('Head Coach', 'Head Coach'), ('Assistant Coach', 'Assistant Coach')], max_length=255, verbose_name='Position')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Coaches',
                'verbose_name': 'Coach',
            },
        ),
        migrations.AlterUniqueTogether(
            name='coach',
            unique_together=set([('user', 'team')]),
        ),
    ]