from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#import DjangoProject.HvZ.views

urlpatterns = patterns(
    '',
    # Example:
    # (r'^DjangoProject/', include('DjangoProject.foo.urls')),

    #(r'^tinymce/', include('tinymce.urls')),
    
    (r'^$', 'DjangoProject.HvZ.views.homepage_view'),
    (r'^twilio/call/$', 'DjangoProject.HvZ.views.twilio_call_view'),
    (r'^twilio/sms/$', 'DjangoProject.HvZ.views.twilio_sms_view'),
    (r'^player/$', 'DjangoProject.HvZ.views.player_user_search'),
    (r'^player/user/(?P<user_name>[\w@\.]+)/$',
     'DjangoProject.HvZ.views.player_user_profile'),
    (r'^player/eat/$', 'DjangoProject.HvZ.views.eat_view'),
    (r'^mission/$', 'DjangoProject.HvZ.views.mission_list_view'),
    (r'^mission/(?P<mission_id>[\d]+)/$',
     'DjangoProject.HvZ.views.mission_json_view'),
    (r'^rules/$', 'DjangoProject.HvZ.views.rules_list_view'),
    (r'^rules/(?P<rule_type>[\w]+)/(?P<rule_id>[\d]+)/$',
     'DjangoProject.HvZ.views.rules_json_view'),
    (r'^timeline/$', 'DjangoProject.HvZ.views.plot_view'),
    (r'^register/$', 'DjangoProject.HvZ.views.register_view'),
    (r'^login/$', 'DjangoProject.HvZ.views.login_view'),
    (r'^logout/$', 'DjangoProject.HvZ.views.logout_view'),
    (r'^forum/$', 'DjangoProject.HvZ.views.forum_thread_view'),
    (r'^forum/reply/$', 'DjangoProject.HvZ.views.forum_new_post_view'),
    (r'^forum/thread/$', 'DjangoProject.HvZ.views.forum_new_thread_view'),
    (r'^forum/(?P<Parent>[\d]+)/$', 'DjangoProject.HvZ.views.forum_post_view'),
    (r'^mobile/eat/$', 'DjangoProject.HvZ.views.mobile_eat_view'),
    (r'^mobile/eat/(?P<FeedCode>[A-Z]{5})/$','DjangoProject.HvZ.views.mobile_eat_view'),
    (r'^attendance/$', 'DjangoProject.HvZ.views.attendance_view'),
    (r'^email/$', 'DjangoProject.HvZ.views.email_view'),
    (r'^dups/$', 'DjangoProject.HvZ.views.duplicate_view'),
    (r'^forgot/$', 'DjangoProject.HvZ.views.not_registered_view'),
    (r'^player/passwordreset/$', 'DjangoProject.HvZ.views.password_reset_view'),
    (r'^player/passwordreset/(?P<hash>[\w]+)/$', 'DjangoProject.HvZ.views.password_reset_view'),

    (r'^status/$','DjangoProject.HvZ.views.stats_home_view'),
    (r'^status/boss$','DjangoProject.HvZ.views.stats_home_fast'),
    (r'^status/(?P<category>[\w]+)/$','DjangoProject.HvZ.views.stats_category_view'),
    (r'^status/(?P<category>[\w]+)/(?P<specific>[\w]+)/$','DjangoProject.HvZ.views.stats_detail_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

"""  
old status
"""
