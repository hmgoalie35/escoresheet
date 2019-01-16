from django.conf.urls import include, url

from seasons.urls import season_roster_urls


urlpatterns = [
    url(r'^(?P<team_pk>\d+)/season-rosters/', include(season_roster_urls, namespace='season_rosters')),
    url(r'^(?P<team_pk>\d+)/games/', include('games.urls', namespace='games')),
]
