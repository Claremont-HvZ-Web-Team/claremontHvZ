from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import DjangoProject.HvZ.views

urlpatterns = patterns(
    '',
    # Example:
    # (r'^DjangoProject/', include('DjangoProject.foo.urls')),

    #(r'^tinymce/', include('tinymce.urls')),

    url('^$', 'DjangoProject.HvZ.views.homepage_view'),
    url('^twilio/call/$', 'DjangoProject.HvZ.views.twilio_call_view'),
    url('^twilio/sms/$', 'DjangoProject.HvZ.views.twilio_sms_view'),
    url('^player/$', 'DjangoProject.HvZ.views.player_user_search'),
    url('^player/user/(?P<user_name>[\w@\.]+)/$',
     'DjangoProject.HvZ.views.player_user_profile'),
    url('^player/eat/$', 'DjangoProject.HvZ.views.eat_view'),
    url('^mission/$', 'DjangoProject.HvZ.views.mission_list_view'),
    url('^mission/(?P<mission_id>[\d]+)/$',
     'DjangoProject.HvZ.views.mission_json_view'),
    url('^rules/$', 'DjangoProject.HvZ.views.rules_list_view'),
    url('^rules/(?P<rule_type>[\w]+)/(?P<rule_id>[\d]+)/$',
     'DjangoProject.HvZ.views.rules_json_view'),
    url('^timeline/$', 'DjangoProject.HvZ.views.plot_view'),
    url('^register/$', DjangoProject.HvZ.views.RegFormView.as_view()),
    url('^login/$', 'DjangoProject.HvZ.views.login_view'),
    url('^logout/$', 'DjangoProject.HvZ.views.logout_view'),
    url('^forum/$', 'DjangoProject.HvZ.views.forum_thread_view'),
    url('^forum/reply/$', 'DjangoProject.HvZ.views.forum_new_post_view'),
    url('^forum/thread/$', 'DjangoProject.HvZ.views.forum_new_thread_view'),
    url('^forum/(?P<Parent>[\d]+)/$', 'DjangoProject.HvZ.views.forum_post_view'),
    url('^mobile/eat/$', 'DjangoProject.HvZ.views.mobile_eat_view'),
    url('^mobile/eat/(?P<FeedCode>[A-Z]{5})/$','DjangoProject.HvZ.views.mobile_eat_view'),
    url('^attendance/$', 'DjangoProject.HvZ.views.attendance_view'),
    url('^email/$', 'DjangoProject.HvZ.views.email_view'),
    url('^dups/$', 'DjangoProject.HvZ.views.duplicate_view'),
    url('^forgot/$', 'DjangoProject.HvZ.views.not_registered_view'),
    url('^player/passwordreset/$', 'DjangoProject.HvZ.views.password_reset_view'),
    url('^player/passwordreset/(?P<hash>[\w]+)/$', 'DjangoProject.HvZ.views.password_reset_view'),

    url('^status/$','DjangoProject.HvZ.views.stats_home_view'),
    url('^status/boss$','DjangoProject.HvZ.views.stats_home_fast'),
    url('^status/(?P<category>[\w]+)/$','DjangoProject.HvZ.views.stats_category_view'),
    url('^status/(?P<category>[\w]+)/(?P<specific>[\w]+)/$','DjangoProject.HvZ.views.stats_detail_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url('^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url('^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url('^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )
