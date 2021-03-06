from django.contrib import admin

from .forms import HockeySeasonRosterAdminForm, SeasonAdminForm
from .models import HockeySeasonRoster, Season


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'season', 'start_date', 'end_date', 'league', 'sport', 'is_past', 'is_current', 'is_future']
    search_fields = ['id', 'start_date', 'end_date']
    filter_horizontal = ['teams']
    form = SeasonAdminForm

    def season(self, obj):
        return str(obj)

    def is_past(self, obj):
        return obj.is_past

    is_past.boolean = True

    def is_current(self, obj):
        return obj.is_current

    is_current.boolean = True

    def is_future(self, obj):
        return obj.is_future

    is_future.boolean = True

    def sport(self, obj):
        return obj.league.sport


@admin.register(HockeySeasonRoster)
class HockeySeasonRosterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'season', 'team', 'division', 'default', 'is_past', 'created_by', 'created']
    search_fields = ['team__name', 'season__start_date', 'season__end_date']
    filter_horizontal = ['players']
    readonly_fields = ['created_by']
    form = HockeySeasonRosterAdminForm

    def save_model(self, request, obj, form, change):
        if obj.created_by is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def division(self, obj):
        return obj.team.division

    def is_past(self, obj):
        return obj.season.is_past

    is_past.short_description = 'Is Past Season'
    is_past.boolean = True
