from django.conf.urls import patterns, url

from HVZ.api.views import json_get_all_emails, Mailer
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = patterns('HVZ.api.views',
    # Replace this view with your own
    url('^emails', staff_member_required(json_get_all_emails)),

    url('^mailer', staff_member_required(Mailer.as_view())),
)
