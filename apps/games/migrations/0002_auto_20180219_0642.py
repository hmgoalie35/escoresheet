# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-19 06:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        ('penalties', '0001_initial'),
        ('locations', '0002_auto_20180219_0642'),
        ('players', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
        ('common', '0001_initial'),
        ('seasons', '0001_initial'),
        ('periods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hockeygoal',
            name='penalty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='penalties.HockeyPenalty', verbose_name='Penalty'),
        ),
        migrations.AddField(
            model_name='hockeygoal',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goals', to='periods.HockeyPeriod', verbose_name='Period'),
        ),
        migrations.AddField(
            model_name='hockeygoal',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goals', to='players.HockeyPlayer', verbose_name='Player'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='away_players',
            field=models.ManyToManyField(related_name='away_games', to='players.HockeyPlayer', verbose_name='Away Roster'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_hockeygames', to='teams.Team', verbose_name='Away Team'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hockeygames_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='home_players',
            field=models.ManyToManyField(related_name='home_games', to='players.HockeyPlayer', verbose_name='Home Roster'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_hockeygames', to='teams.Team', verbose_name='Home Team'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hockeygames', to='locations.Location', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='point_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='common.GenericChoice', verbose_name='Point Value'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hockeygames', to='seasons.Season', verbose_name='Season'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='teams.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='hockeygame',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='common.GenericChoice', verbose_name='Game Type'),
        ),
        migrations.AddField(
            model_name='hockeyassist',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assists', to='games.HockeyGoal', verbose_name='Goal'),
        ),
        migrations.AddField(
            model_name='hockeyassist',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assists', to='players.HockeyPlayer', verbose_name='Player'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='away_players',
            field=models.ManyToManyField(related_name='away_games', to='players.BaseballPlayer', verbose_name='Away Roster'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_baseballgames', to='teams.Team', verbose_name='Away Team'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='baseballgames_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='home_players',
            field=models.ManyToManyField(related_name='home_games', to='players.BaseballPlayer', verbose_name='Home Roster'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_baseballgames', to='teams.Team', verbose_name='Home Team'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='baseballgames', to='locations.Location', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='point_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='common.GenericChoice', verbose_name='Point Value'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='baseballgames', to='seasons.Season', verbose_name='Season'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='teams.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='baseballgame',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='common.GenericChoice', verbose_name='Game Type'),
        ),
        migrations.AlterUniqueTogether(
            name='hockeyassist',
            unique_together=set([('player', 'goal')]),
        ),
    ]
