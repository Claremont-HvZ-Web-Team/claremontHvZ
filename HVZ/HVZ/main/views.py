from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView

from HVZ.feed.models import Meal
# Create your views here.


class LandingPage(TemplateView):
    template_name = "main/landing_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(LandingPage, self).get_context_data(*args, **kwargs)

        if not self.request.user.is_authenticated():
            form = AuthenticationForm()
        else:
            form = None

        context['login_form'] = form
        context['is_landing_page'] = True
        context['latest_meals'] = Meal.objects.all().order_by('time')[:20]
        return context
