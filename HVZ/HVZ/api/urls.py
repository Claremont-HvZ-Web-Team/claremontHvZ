from django.conf.urls import patterns, url

from HVZ.api.views import json_get_all_emails

urlpatterns = patterns('HVZ.api.views',
    # Replace this view with your own
    url('^emails', json_get_all_emails),
)
