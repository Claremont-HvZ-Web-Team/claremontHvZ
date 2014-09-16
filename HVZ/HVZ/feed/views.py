from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from HVZ.main.decorators import team_required, require_active_game

from models import Meal, Player
from forms import MealForm, DonateForm


class EatView(FormView):
    form_class = MealForm
    template_name = "feed/eat.html"

    @method_decorator(login_required)
    @method_decorator(require_active_game)
    @method_decorator(team_required('Z'))
    def dispatch(self, *args, **kwargs):
        return super(EatView, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        form = super(FormView, self).get_form(form_class)
        form.initial = self.kwargs
        return form

    def get_success_url(self):
        return reverse("main_landing")

    def form_valid(self, form):
        def grab(s):
            return form.cleaned_data[s]
        zombie = Player.logged_in_player(self.request)
        victim = Player.current_players().select_for_update().get(feed=grab("feedcode"))
        m = Meal(
            eater=zombie,
            eaten=victim,
            time=grab('time'),
            location=grab("location"),
            description=grab("description"),
        )
        m.full_clean()
        m.save()
        
        
        return super(EatView, self).form_valid(form)




class DonateView(FormView):
    form_class = DonateForm
    template_name = "feed/donate.html"

    @method_decorator(login_required)
    #@method_decorator(require_active_game)
    @method_decorator(team_required('Z'))
    def dispatch(self, *args, **kwargs):
        return super(DonateView,self).dispatch(*args,**kwargs)

    def get_form(self,form_class):
        form = super(FormView, self).get_form(form_class)
        form.initial = self.kwargs
        return form

    @method_decorator(never_cache)
    def get(self,request):
        form = self.get_form(self.form_class)
        template = loader.get_template(self.template_name)
        thisPlayer = Player.logged_in_player(request)
        contextDict = {
            "donator_meals" : thisPlayer.brains,
            "form" : form,
        }
        context = RequestContext(request,contextDict)
        return HttpResponse(template.render(context))

    def get_success_url(self):
        # TODO Should this have a confirmation? Or 
        # possibly go back to the same page to donate
        # to a different person?
        return reverse("player_list")

    


    def form_valid(self,form):
        def grab(s):
            return form.cleaned_data[s]

        donatingPlayer = Player.logged_in_player(self.request)
        receivingPlayer = grab('receiver')
        brains = grab('numberOfMeals')

        
        donatingPlayer.brains -= brains
        receivingPlayer.brains += brains
        donatingPlayer.save()
        receivingPlayer.save()

        return super(DonateView, self).form_valid(form)

    