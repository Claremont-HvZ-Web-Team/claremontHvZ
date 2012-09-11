from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #Load tinymce urls first
    #(r'^tinymce/', include('tinymce.urls')),

    #Home page
    (r'^$', 'HvZ.views.homepage_view'),

    #Rules
    #Landing page for rules
    (r'^rules/$', 'HvZ.views.rules_list_view'),
    #Expand details for specific rule
    (r'^rules/(?P<rule_id>[\d]+)/$', 'HvZ.views.dummy'),

    #Graphs
    #Landing page for graphs
    (r'^graphs/$', 'HvZ.views.dummy'),
    #Page for graph categories (i.e. school, year, or dorm)
    (r'^graphs/(?P<category>[\w+])/$', 'HvZ.views.dummy'),
    #Page for graph subcategories (e.g. Mudd, 2015, or East)
    (r'^graphs/(?P<category>[\w+])/(?P<subcategory>[\w+])/$', 'HvZ.views.dummy'),

    #Players
    #Landing page for players that displays details of each current player in datatables list
    (r'^players/$', 'HvZ.views.dummy'),
    #Player Profile
    (r'^players/profile/(?P<user_name>[\S+])/$', 'HvZ.views.dummy'),
    #Squad Profile
    (r'^players/squad/(?P<group_id>[\d+])/$', 'HvZ.views.dummy'),
    #Achievement Profile
    (r'^players/achievement/(?P<achievement_id>[\d+])/$', 'HvZ.views.dummy'),
    #Player search; take them to the datatables page but prepopulate the filter with their term
    (r'^players/search/(?P<search_term>[.*])/$', 'HvZ.views.dummy'),

    #Forums
    #Landing page for forum, has forums on the left and threads in the selected forum on the right
    (r'^forum/$', 'HvZ.views.dummy'),
    #Returns the right hand side of the page (the posts for a given thread)
    (r'^forum/thread/(?P<thread>[\d]+)/$', 'HvZ.views.dummy'),
    #Page where new threads and posts are submitted to
    (r'^forum/post/$', 'HvZ.views.dummy'),

    #Missions
    #Mission landing page
    (r'^mission/$', 'HvZ.views.dummy'),
    #JSON of mission details
    (r'^mission/(?P<mission_id>[\d]+)/$', 'HvZ.dummy'),

    #Game Actions
    #Eat
    (r'^game/eat/$', 'HvZ.dummy'),
    #Decode (a mission specific page that lets humans decrypt messages and displays a substitution cipher for zombies)
    (r'^game/decode/$', 'HvZ.dummy'),

    #Player Settings
    #Change how you view the website (force background color, increase font size, etc)
    (r'^settings/web/$', 'HvZ.views.dummy'),
    #Change how others view your profile (profile pic, who can see your cell, etc)
    (r'^settings/profile/$', 'HvZ.views.dummy'),
    #Change your user information (name, dorm, school)
    (r'^settings/user/$', 'HvZ.views.dummy'),
    #Change the settings for a squad you are in charge of (name, pic, etc)
    (r'^settings/squad/$', 'HvZ.views.dummy'),

    #Authentication
    #Game registration
    (r'^auth/register/$', 'HvZ.views.dummy'),
    #Login to the website
    (r'^auth/login/$', 'HvZ.views.dummy'),
    #Logout from the website
    (r'^auth/logout/$', 'HvZ.views.dummy'),
    #When you click "I forgot my password" go here
    (r'^auth/forgot/$', 'HvZ.views.dummy'),
    #Once they click the link in their email to reset their password, go here
    (r'^auth/reset/(?P<hash>[\w]+)/$', 'HvZ.views.dummy'),

    #Twilio
    #Call forwarding
    (r'^twilio/call/$', 'HvZ.views.dummy'),
    #Text message handling
    (r'^twilio/sms/$', 'HvZ.views.dummy'),

    #Mobile site
    #Page for eating. This is for when they lack a QR code to eat
    (r'^mobile/eat/$', 'HvZ.views.dummy'),
    #Page for eating. Players are directed here if they scan a QR code
    (r'^mobile/eat/(?P<FeedCode>[A-Z]{5})/$', 'HvZ.views.dummy'),

    #Moderator tools (if they can't somehow be done in the admin panel)
    #A grid of all players by all missions so they can check attendance off
    (r'^moderator/attendance/$', 'HvZ.views.dummy'),
    #The page for moderators to send emails to players from
    (r'^moderator/email/$', 'HvZ.views.dummy'),

    #About us pages
    #about HvZ as a whole
    (r'^about/HvZ/$', 'HvZ.views.dummy'),
    #mod team profiles
    (r'^about/mod/$', 'HvZ.views.dummy'),
    #how you can help us
    (r'^about/help/$', 'HvZ.views.dummy'),
    #how to contact the mod team or find us on other websites (like facebook)
    (r'^about/contact/$', 'HvZ.views.dummy'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^{0}(?P<path>.*)$'.format(settings.STATIC_URL),
            'django.views.static.serve', {
                'document_root': settings.STATIC_ROOT,
            }),
    )
