from django.conf.urls import patterns, url

from HVZ.missions import views

urlpatterns = patterns('HVZ.missions.views',
    url(r'^$', views.PlotListView.as_view(), name="plot_list"),
    url(r'^(?P<pk>[\d]+)/(?P<slug>[-_\w]+)/$',
        views.PlotDetailView.as_view(),
        name="plot_detail"),
)
