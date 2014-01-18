from django.conf.urls import patterns, url

from HVZ.forum.views import (
    CurrentGameThreadsView, ThreadCreate, thread_detail_view
)

urlpatterns = patterns(
    'HVZ.forum.views',
    url(r'^$', CurrentGameThreadsView.as_view(), name="current_game_threads"),
    url(r'^threads/$', ThreadCreate.as_view(), name="thread_create"),
    url(r'^threads/(?P<pk>[\d]+)/(?P<slug>[-_\w]+)/$', thread_detail_view, name="thread_detail"),
)
