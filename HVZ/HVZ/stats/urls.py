from django.conf.urls import patterns, url

from views import (
    PopStatPage,
    AncestryPage,
    OutbreakPage,
    MealLog,
    JSONPlayerStats,
    JSONZombieAncestry,
    JSONOutbreak,
    JSONPopulationTimeSeries,
)


urlpatterns = patterns('HVZ.stats.views',
    url(r'^$', PopStatPage.as_view(), name='stats_list'),
    url(r'^tags', MealLog.as_view(), name='stats_meal_log'),
    url(r'^outbreak', OutbreakPage.as_view(), name='stats_outbreak'),
    url(r'^ancestry', AncestryPage.as_view(), name='stats_ancestry'),
    url(r'^json/players.json', JSONPlayerStats.as_view(), name="data_players"),
    url(r'^json/ancestry.json', JSONZombieAncestry.as_view(), name="data_ancestry"),
    url(r'^json/taghistogram.json', JSONOutbreak.as_view(), name="data_meal_histogram"),
    url(r'^json/poptimeseries.json',
        JSONPopulationTimeSeries.as_view(),
        name="data_pop_time_series"),
)
