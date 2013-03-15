from django.views.generic import TemplateView


class FullStatPage(TemplateView):
    template_name = 'stats/the_stats.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FullStatPage, self).get_context_data(*args, **kwargs)

        return context
