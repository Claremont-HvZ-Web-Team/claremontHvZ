from django.conf import urls

from HVZ.rules import views

urlpatterns = urls.patterns(
    'HVZ.rules.views',
    urls.url(r'^$', views.RulesPage.as_view(), name="rules"),
)
