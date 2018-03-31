import calendar
import collections
import datetime as dt
import json

from django import db, urls
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import permission_required, login_required
from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.http import HttpResponse

from hvz.main import decorators, forms, mixins, models

def landing_page(request):
    context = {}

    if not request.user.is_authenticated:
        form = forms.PrettyAuthForm()
    else:
        form = None

    context['login_form'] = form
    context['is_landing_page'] = True
    try:
        context['latest_meals'] = models.Meal.objects.filter(
            eater__game=models.Game.objects.latest(),
        ).order_by('-time')[:20]
    except models.Game.DoesNotExist:
        context['latest_meals'] = []

    return render(request, "landing_page.html", context)

def logout(request):
    auth_logout(request)
    return landing_page(request)

def register_success(request):
    return render(request, 'register_success.html', {})

class RegisterView(generic.FormView):
    form_class = forms.RegisterForm
    template_name = "register.html"

    @method_decorator(permission_required("main.add_player"))
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return urls.reverse(register_success)

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)

class EatView(generic.FormView):
    form_class = forms.MealForm
    template_name = "eat.html"

    @method_decorator(login_required)
    @method_decorator(decorators.team_required('Z'))
    def dispatch(self, *args, **kwargs):
        return super(EatView, self).dispatch(*args, **kwargs)

    def get_form(self):
        form = super(generic.FormView, self).get_form(self.form_class)
        form.initial = self.kwargs
        return form

    def get_success_url(self):
        return urls.reverse(landing_page)

    def form_valid(self, form):
        def grab(s):
            return form.cleaned_data[s]
        zombie = models.Player.logged_in_player(self.request)
        victim = models.Player.current_players().select_for_update().get(
            feed=grab("feedcode")
        )
        m = models.Meal(
            eater=zombie,
            eaten=victim,
            time=grab('time'),
            description=grab("description"),
        )
        m.full_clean()
        m.save()

        return super(EatView, self).form_valid(form)

def player_list(request):
    school = request.GET.get('school')
    gradyear = request.GET.get('gradyear')

    context = {}

    queryset = models.Player.current_players()

    if gradyear:
        queryset = queryset.filter(grad_year=gradyear)

    if school:
        queryset = queryset.filter(
            school__name__istartswith=school
        )

    players = (
        queryset.select_related('school').
        annotate(meal_count=db.models.Count('meal_set')).
        order_by('-meal_count')
    )

    context['humans'] = [p for p in players if p.team == 'H']
    context['zombies'] = [p for p in players if p.team == 'Z']

    context['game_season'] = models.Game.nearest_game().season()

    context['schools'] = models.School.objects.all().annotate(
        num_players=db.models.Count('player_set')
    ).order_by('-num_players')

    context['years'] = sorted(set([
        player.grad_year for player in players
        if player.grad_year is not None
    ]))

    context['school'] = school
    context['gradyear'] = gradyear

    return render(request, 'player_list.html', context)

class PlayerEmailView(generic.ListView):
    model = models.Player
    template_name = 'players/email_list.html'

    def get_queryset(self):
        game = models.Game.nearest_game()
        return models.Player.objects.filter(game=game)


class DonateView(generic.FormView):
    form_class = forms.DonateForm
    template_name = "donate.html"

    @method_decorator(login_required)
    @method_decorator(decorators.team_required('Z'))
    def dispatch(self, *args, **kwargs):
        return super(DonateView,self).dispatch(*args,**kwargs)

    def get_success_url(self):
        return urls.reverse('donate_success')

    def get_form_kwargs(self):
        kwargs = super(DonateView, self).get_form_kwargs()
        kwargs['donor'] = models.Player.logged_in_player(self.request)
        return kwargs

    def form_valid(self,form):
        def grab(s):
            return form.cleaned_data[s]

        donor = models.Player.logged_in_player(self.request)
        receiver = grab('receiver')
        num_brains = grab('num_brains')

        donor.brains -= num_brains
        receiver.brains += num_brains

        with transaction.atomic():
            donor.save()
            receiver.save()

        return super(DonateView, self).form_valid(form)

### STATS PAGE ###

class PopStatPage(generic.TemplateView):
    template_name = 'pop_stats.html'


class MealLog(generic.ListView):
    template_name = 'meal_log.html'

    def get_queryset(self, *args, **kwargs):
        return (
            models.Meal.objects.filter(
                eater__game=models.Game.nearest_game()
            ).select_related(
                'eater__user',
                'eaten__user',
            ).order_by('time')
        )

class AncestryPage(generic.TemplateView):
    template_name = 'ancestry.html'


class OutbreakPage(generic.TemplateView):
    template_name = 'outbreak.html'

def json_format_time(datetime_object):
    """Convert a Python datetime object to a JS timestamp"""
    if timezone.is_naive(datetime_object):
        datetime_object = timezone.make_aware(
            datetime_object,
            timezone.get_default_timezone(),
        )

    return calendar.timegm(datetime_object.utctimetuple()) * 1000

def json_population_time_series(request):
    context = models.Meal.objects.filter(
        eater__game=models.Game.nearest_game(),
        time__isnull=False,
    )
    game = models.Game.nearest_game()

    t0, tf = time_endpoints(game)

    players = models.Player.current_players().all()
    meals = models.Meal.objects.select_related('eaten').all()
    eaten_zombies = set([m.eaten for m in meals])
    ozs = [p for p in players if p.team == 'Z' and p not in eaten_zombies]

    num_zombies = len(ozs)
    num_humans = len(players) - num_zombies

    human_tally = []
    zombie_tally = []

    meals_vs_hours = meals_per_hour(game, context)
    for hour in range(len(meals_vs_hours)):
        t = t0 + dt.timedelta(hours=hour)

        # Stop the graph at the current time
        if t > settings.NOW():
            break

        meal_count = meals_vs_hours[hour]

        num_humans -= meal_count
        num_zombies += meal_count

        human_tally.append([json_format_time(t), num_humans])
        zombie_tally.append([json_format_time(t), num_zombies])

    if not human_tally:
        human_tally = [[json_format_time(t0), num_humans]]

    if not zombie_tally:
        zombie_tally = [[json_format_time(t0), num_zombies]]

    return mixins.json_response([
        {'label': 'humans', 'data': human_tally, 'color': 'rgb(128, 0, 0)'},
        {'label': 'zombies', 'data': zombie_tally, 'color': 'rgb(0, 128, 0)'},
    ])

def json_get_all_emails(request):
    """A function that displays all emails.
    """
    emails = [p.user.email for p in models.Player.current_players()]
    
    # json.dumps creates a string from a Python object.
    json_data = json.dumps(emails)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )

def success(request):
    return render(request, 'api/success.html', {})


def time_endpoints(game):
    """Return the start and end times of the game.

    Assume we start at 8am and finish at 11pm, and assume a game lasts
    seven days.

    """
    t0 = timezone.make_aware(
        dt.datetime.combine(game.start_date, dt.time(hour=8))
    )
    tf = timezone.make_aware(
        dt.datetime.combine(
            game.start_date,
            dt.time(hour=23),
        ) + dt.timedelta(days=7)
    )

    return t0, tf

def json_tag_histogram(request):
    context = models.Meal.objects.filter(
        eater__game=models.Game.nearest_game(),
        time__isnull=False,
    )
    game = models.Game.nearest_game()
    t0, tf = time_endpoints(game)

    meals_vs_hours = meals_per_hour(
        models.Game.nearest_game(),
        context,
    )

    histogram = []
    for hour in range(len(meals_vs_hours)):
        t = t0 + dt.timedelta(hours=hour)

        # Stop at the current time
        if t > settings.NOW():
            break

        histogram.append([json_format_time(t), meals_vs_hours[hour]])

    # Pre-game case
    if not histogram:
        histogram = [[json_format_time(t0), 0]]

    return mixins.json_response([{
        "data": histogram,
        "color": "rgb(0, 128, 0)",
    }])

def meals_per_hour(game, meals):
    """Return the number of meals in each hour between now and the game's end."""
    # If we got a queryset, evaluate it now.
    meals = list(meals)

    t0, tf = time_endpoints(game)

    meals_vs_hours = collections.defaultdict(int)
    for m in meals:
        num_hours = hours_between(m.time, t0)
        meals_vs_hours[num_hours] += 1

    num_hours = int(hours_between(tf, t0))
    aggregates = []
    for hour in range(num_hours):
        aggregates.append(meals_vs_hours[hour])

    return aggregates


def hours_between(t1, t2):
    dt = abs(t2 - t1)
    return dt.days*24 + dt.seconds/3600


def json_zombie_ancestry(request):
    players = models.Player.current_players().filter(
        team='Z'
    ).select_related('user')
    names = {p: p.user.get_full_name() for p in players}
    meals = models.Meal.objects.filter(
        eater__game=models.Game.nearest_game()
    ).select_related('eater', 'eaten')

    possible_ozs = set([p for p in players])
    children = collections.defaultdict(list)
    for m in meals:
        if m.eaten not in players:
            continue
        children[m.eater].append(m.eaten)
        if m.eaten in possible_ozs:
            possible_ozs.remove(m.eaten)

    ozs = [p for p in players if p in possible_ozs]

    def traverse(zombie):
        """Return a nested tree of the given zombie and all its children"""
        return {
            "name": names[zombie],
            "children": [traverse(c) for c in children[zombie]],
        }

    return mixins.json_response({
        "name": "Subject Zero",
        "children": [traverse(z) for z in ozs],
    })


def json_player_stats(request):
    FIELDS = ('team', 'grad_year', 'school_id', 'dorm_id')

    def _bounded_grad_year(grad_year):
        return abs(models.Game.nearest_game().start_date.year - grad_year) < 5

    aggregates = {
        'grad_year': [
            {'label': 'zombies', 'data': collections.defaultdict(int), 'color': 'rgb(0, 128, 0)'},
            {'label': 'humans', 'data': collections.defaultdict(int), 'color': 'rgb(128,0,0)'},
        ],
        'dorm_id': [
            {'label': 'zombies', 'data': collections.defaultdict(int), 'color': 'rgb(0, 128, 0)'},
            {'label': 'humans', 'data': collections.defaultdict(int), 'color': 'rgb(128,0,0)'},
        ],
        'school_id': [
            {'label': 'zombies', 'data': collections.defaultdict(int), 'color': 'rgb(0, 128, 0)'},
            {'label': 'humans', 'data': collections.defaultdict(int), 'color': 'rgb(128,0,0)'},
        ],
    }

    dorms = models.Building.objects.filter(
        building_type="D"
    ).order_by("name").values('id', 'name')

    player_dicts = models.Player.current_players().values()

    dorm_ordering = list(b['id'] for b in dorms)
    dorm_name_ordering = list(b['name'] for b in dorms)
    axis_lookup = {
        'grad_year': {},  # 2013, etc.
        'dorm_id': dict(enumerate(dorm_name_ordering)),  # 0: Atwood Dorm, etc.
        'school_id': {
            d['id']: d['name'] for d in
            models.School.objects.order_by('name').values(
                'id',
                'name',
            )
        },
    }


    for item in player_dicts:
        index = 0 if item['team'] == "Z" else 1

        if item['grad_year']:

            axis_lookup['grad_year'].setdefault(item['grad_year'], str(item['grad_year']))

        for key in aggregates:
            if item[key]:
                try:
                    if key == 'grad_year' and not _bounded_grad_year(item['grad_year']):
                        continue

                    if key == 'dorm_id':
                        if item[key] in dorm_ordering:
                            aggregates[key][index]['data'][dorm_ordering.index(item[key])] += 1
                    else:
                        aggregates[key][index]['data'][item[key]] += 1
                except KeyError:
                    continue

    aggregates['ticks'] = axis_lookup
    # convert all data dicts to arrays
    for key in aggregates:
        if key == "ticks":
            for tick_set in aggregates[key]:
                aggregates[key][tick_set] = [
                    [int(_id), val] for _id, val in
                    aggregates[key][tick_set].items()
                ]
            continue
        for data_set in aggregates[key]:
            if key == 'dorm_id':
                # flip dorm data series for horizontal bars
                data_set['data'] = [
                    [val, dkey] for dkey, val in
                    data_set['data'].items()
                ]
                data_set['data'].sort(key=(lambda x: x[1]))
            else:
                data_set['data'] = [
                    [dkey, val] for dkey, val in
                    data_set['data'].items()
                ]
                data_set['data'].sort(key=(lambda x: x[0]))

    return mixins.json_response(aggregates)


class HarrassmentView(generic.FormView):
    template_name = "main/harrassmentForm.html"
    form_class = forms.HarrassmentForm

    def dispatch(self, *args, **kwargs):
        return super(HarrassmentView,self).dispatch(*args,**kwargs)

    def get_success_url(self):
        return urls.reverse(harrassmentConfirmation)

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
