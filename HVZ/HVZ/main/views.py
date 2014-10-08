from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.conf import settings

from HVZ.main.models import Game, ModSchedule, Player
from HVZ.feed.models import Meal
from HVZ.main.forms import PrettyAuthForm, RegisterForm, HarrassmentForm
from HVZ.main.decorators import require_unfinished_game


class LandingPage(TemplateView):
    template_name = "main/landing_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(LandingPage, self).get_context_data(*args, **kwargs)

        if not self.request.user.is_authenticated():
            form = PrettyAuthForm()
        else:
            form = None

        context['login_form'] = form
        context['is_landing_page'] = True
        try:
            context['latest_meals'] = (
                Meal.objects.filter(
                    eater__game=Game.games(started=True).latest(),
                ).order_by('-time')[:20])
        except Game.DoesNotExist:
            context['latest_meals'] = []

        return context


class Register(FormView):
    form_class = RegisterForm
    template_name = "main/register.html"

    @method_decorator(permission_required("main.add_player"))
    @method_decorator(require_unfinished_game)
    def dispatch(self, *args, **kwargs):
        return super(Register, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("success")

    def form_valid(self, form):
        form.save()
        return super(Register, self).form_valid(form)

def success(request):
    return render(request, 'main/success.html', {})

def spitList(request, clan):
    if request.user.is_staff:
        clan = clan.replace("_", " ")
        context = {'clan': clan, 'players':Player.objects.all().filter(game=Game.nearest_game(), clan=clan)}
    else:
        context = {'clan': 'No Permission', 'players':[]}
    return render(request, 'main/spitList.html', context)


class TwilioCallHandler(TemplateView):
    template_name = "main/call.xml"

    def render_to_response(self, context, **kwargs):
        return super(TwilioCallHandler, self).render_to_response(
            context,
            content_type='text/xml',
            **kwargs
        )

    def get_context_data(self, *args, **kwargs):
        context = super(TwilioCallHandler, self).get_context_data(*args, **kwargs)
        on_duty = ModSchedule.get_current_mod()
        if on_duty:
            context["name"] = on_duty.user.first_name
            context["cell"] = on_duty.cell
        else:
            # this should NOT HAPPEN
            pass

        return context


class HarrassmentView(FormView):
    template_name = "main/harrassmentForm.html"
    form_class = HarrassmentForm

    
    def dispatch(self, *args, **kwargs):
        return super(HarrassmentView,self).dispatch(*args,**kwargs)

    def get_success_url(self):
        return reverse("harrassmentConfirmation")

    def form_valid(self, form):
        description = form.cleaned_data['description']
        toAddress = settings.MODERATOR_EMAIL
        if (form.cleaned_data['anonymous']):
            # Send email anonymously
            fromAddress = settings.ANON_HARRASSMENT_EMAIL
        else :
            # Send data from users email
            thisUser = self.request.user
            fromAddress = thisUser.email
        
        send_mail('Harrassment Complaint',description,fromAddress,[toAddress],fail_silently=False)    
        
        return super(HarrassmentView,self).form_valid(form)

def harrassmentConfirmation(request):
    return render(request,"main/harrassmentConfirmation.html",{})