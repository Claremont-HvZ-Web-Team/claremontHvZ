from django.views import generic

from HVZ.rules import models

class RulesPage(generic.TemplateView):
    template_name = "rules/rules.html"

    def get_context_data(self, *args, **kwargs):
        context = super(RulesPage, self).get_context_data(*args, **kwargs)

        context['core'] = models.CoreRule.objects.all()
        context['locations'] = models.LocationRule.objects.all()
        context['classes'] = models.ClassRule.objects.all()
        context['specialinfected'] = models.SpecialInfectedRule.objects.all()
        context['locations'] = models.LocationRule.objects.all()

        return context
