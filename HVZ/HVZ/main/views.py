from django.views.generic import TemplateView

# Create your views here.


class LandingPage(TemplateView):
    template_name = "main/landing_page.html"
