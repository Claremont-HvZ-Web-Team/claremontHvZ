from hvz_utils import *
from django.db.models import Q
from django.views.decorators.cache import cache_page


def elapsed_hours(t, t0):
    """Return the number of elapsed hours between t and t0"""
    dt = t - t0
    return (dt.days * 24) + (dt.seconds // 3600)


def meal_histograms(g):
    """Generate two dictionaries used to display the cumulative and meal density graphs."""
    # 10 is the number of OZs + mod listed as starting zed + press
    # account
    hum = Registration.objects.filter(game=g).count() - 10
    zom = 10

    t0 = datetime.combine(g.start_date, time(8))
    dt = timedelta(hours=1)

    """tf is the earlier of now or the game's end time"""
    end = datetime.combine(g.start_date, time(21)) + timedelta(days=4)
    tf = datetime.now()
    if end < tf:
        tf = end

    num_hours = elapsed_hours(tf, t0) + 1

    # Initialize a list of buckets - - - one for each hour
    meals_per_hour = [0 for i in xrange(num_hours)]

    # Make one query to the database, then drop each meal in its
    # appropriate bucket.
    meal_query = Meal.objects.all()
    for m in meal_query:
        t = m.time
        i = elapsed_hours(t, t0)
        meals_per_hour[i] += 1

    # Number of kills in each hour
    per_hour = []

    # Cumulative graph of kills per hour
    upto_hour = []

    t = t0
    for i in xrange(num_hours):
        per_hour += [{"hour": t, "meals": meals_per_hour[i]}]
        hum -= meals_per_hour[i]
        zom += meals_per_hour[i]
        upto_hour += [{"hour": t + dt, "humans": hum, "zombies": zom}]
        t += dt

    return (per_hour, upto_hour)


# Todo: make a separate file of query templates and document them.
def jsonify(query):
    cursor = connection.cursor()
    cursor.execute(query)
    key_val_pairs = [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]
    return [dict(line) for line in key_val_pairs]


def get_stat(game, constraints):
    # This should actually be called get_count, you nooblings
    baseQuery = Character.objects.filter(constraints, game=game).count()

    return baseQuery


def school_team_counts(game):
    """Get the number of humans and zombies per school."""
    all_schools = School.objects.all()

    school_scores = {}
    for s in all_schools:
        school_scores[s] = {
            'name': s.name,
            'humans': get_stat(game, Q(team='H', player__school=s)),
            'zombies': get_stat(game, Q(team='Z', player__school=s))
        }
    return school_scores.values()


def year_team_counts(game):
    """Get the number of humans and zombies per year."""
    # We should do something better than this with our constants!
    # For some reason, this function used to return nonzero graduates for 2019. That's been fixed.
    y0 = 2012
    yf = 2020
    return [{
        "year": y,
        "humans": get_stat(game, Q(team='H', player__class_year=str(y))),
        "zombies": get_stat(game, Q(team='Z', player__class_year=str(y)))}
         for y in (y0, yf)]


def stats_home_view(request):
    return stats_home(request, "stats / stat_home.html")


def stats_home_fast(request):
    return stats_home(request, "stats / stat_home_fast.html")


def stats_home(request, template):
    g = get_current_game()
    ui = get_user_info(request)
    all = Registration.objects.filter(game=g).select_related()
    humans = all.filter(team="H")
    zombies = all.filter(team="Z")

    schools = school_team_counts(g)

    years = year_team_counts(g)

    all_dorms = Building.objects.filter(building_type="D")
    dorms = dorm_populations(all_dorms, g)

    human_list = jsonify("select username as user_name, first_name as first, last_name as last, upgrade as class from HvZ_registration, HvZ_player, auth_user where player_id=HvZ_player.id and user_id=auth_user.id and team='H' and game_id=" + str(g.id))

    # I know the SQL here is a mess; MySQL apparently doesn't support "with" clauses.
    zombie_list = jsonify("select username as user_name, first_name as first, last_name as last, meals, upgrade as class from HvZ_registration, HvZ_player, auth_user, (select eater_id, count( * ) as meals from HvZ_meal where game_id=" + str(g.id) + " group by eater_id) as HvZ_mealcounts where player_id=eater_id and player_id=HvZ_player.id and user_id=auth_user.id and team='Z' and game_id=" + str(g.id))

    # This is a good example of how to use select_related. Notice
    # how, below, we're going to draw from the location,
    # eater.user, and eaten.user fields? select_related lets us
    # draw all these fields out with just one query!
    meal_db = Meal.objects.filter(game=g).select_related("location__name",
                                 "location__campus",
                                 "eater__user",
                                 "eaten__user")

    meals = []
    for m in meal_db:
        f_eater = "<a href=' / player / user / " + str(m.eater.user.username) + "' class='hoverme' > " + str(m.eater) + "</span> "
        f_eaten = "<a href=' / player / user / " + str(m.eaten.user.username) + "' class='hoverme' > " + str(m.eaten) + "</span> "
        meals.append({
            'eater': f_eater,
            'eaten': f_eaten,
            'when': m.time.strftime(' % a %I: % M%p'),
            'o_time': m.time.isoformat(' '),
            'location': str(m.location),
            'description': m.description,
            'timestamp': datetime.now()
        })

    per_hour, upto_hour = meal_histograms(g)

    return render_to_response(template,
        {
            "user": ui,
            'humans': humans.count(),
            'zombies': zombies.count(),
            'schools': schools,
            'years': years,
            'dorms': dorms,
            'meals': meals,
            'mph': per_hour,
            'mun': upto_hour,
            'human_list': human_list,
            'zombie_list': zombie_list,
        },
        context_instance=RequestContext(request))


def dorm_populations(dorms, game):
    scores = {}
    for d in dorms.select_related("campus"):
        scores[d] = {
            'name': str(d),
            'id': str(d.id),
            'humans': get_stat(game, Q(team='H', player__dorm=d)),
            'zombies': get_stat(game, Q(team='Z', player__dorm=d)),
        }
    return scores.values()


@cache_page(60 * 5)
def stats_category_view(request, category):
    g = get_current_game()
    ui = get_user_info(request)
    all = Registration.objects.filter(game=g)
    data = []
    if category == "school":
        for s in School.objects.all().order_by("name"):
            school_human = all.filter(player__school=s, team="H").count()
            school_zombie = all.filter(player__school=s, team="Z").count()
            if school_human + school_zombie > 0:
                data.append({'id': s.id, 'name': str(s), 'humans': school_human, 'zombies': school_zombie})
    elif category == "dorm":
        for d in Building.objects.filter(building_type="D").order_by("name"):
            dorm_human = all.filter(player__dorm=d, team="H").count()
            dorm_zombie = all.filter(player__dorm=d, team="Z").count()
            if dorm_human + dorm_zombie > 0:
                data.append({'id': d.id, 'name': str(d), 'humans': dorm_human, 'zombies': dorm_zombie})
    elif category == "year":
        for y in range(2011, 2020):
            year_human = all.filter(player__grad_year=y, team="H").count()
            year_zombie = all.filter(player__grad_year=y, team="Z").count()
            if year_human + year_zombie > 0:
                data.append({'id': y, 'name': str(y), 'humans': year_human, 'zombies': year_zombie})
    elif category == "human" or category == "zombie":
        if category == "human":
            players = all.filter(team="H")
        else:
            players = all.filter(team="Z")

        school = []
        for s in School.objects.all().order_by("name"):
            count = players.filter(player__school=s).count()
            if count > 0:
                school.append({'name': str(s), 'members': count})

        dorm = []
        for d in Building.objects.filter(building_type="D").order_by("name"):
            count = players.filter(player__dorm=d).count()
            if count > 0:
                dorm.append({'name': str(d), 'members': count})

        year = []
        for y in range(2011, 2020):
            count = players.filter(player__grad_year=y).count()
            if count > 0:
                year.append({'name': str(y), 'members': count})

        player_list = []
        for r in players:
            pdata = dict()
            pdata['first'] = r.player.user.first_name
            pdata['last'] = r.player.user.last_name
            pdata['school'] = r.player.school
            pdata['year'] = r.player.grad_year
            pdata['class'] = r.upgrade
            if category == "zombie":
                pdata["meals"] = r.get_meals(g)
            else:
                pdata["hardcore"] = r.hardcore
            player_list.append(pdata)

    if category in ["school", "dorm", "year"]:
        return render_to_response('stats / stat_category.html',
            {
                "user": ui,
                'data': data,
            },
            context_instance=RequestContext(request))
    else:
        return render_to_response('stats / stat_team.html',
            {
                "user": ui,
                'category': category,
                'schools': school,
                'years': year,
                'dorms': dorm,
                'player_list': player_list,
            },
            context_instance=RequestContext(request))


@cache_page(60 * 5)
def stats_detail_view(request, category, specific):
    ui = get_user_info(request)
    from django.db.models import Q
    g = get_current_game()
    ui = get_user_info(request)
    all = Registration.objects.filter(game=g)
    humans = all.filter(team="H")
    zombies = all.filter(team="Z")

    if category == "school":
        big = School.objects.filter(name=specific)[0]
        cat = big.name
        big_human = humans.filter(player__school=big)
        big_zombie = zombies.filter(player__school=big)
        meal_list = Meal.objects.filter(game=g).filter(Q(eaten__school=big) | Q(eater__school=big) | Q(location__campus=big))
        dorm_list = Building.objects.filter(building_type="D").filter(Q(campus=big) | Q(campus=None))
    if category == "dorm":
        big = Building.objects.filter(id=specific)[0]
        cat = big.name
        big_human = humans.filter(player__dorm=big)
        big_zombie = zombies.filter(player__dorm=big)
        meal_list = Meal.objects.filter(game=g).filter(Q(eaten__dorm=big) | Q(eater__dorm=big) | Q(location=big))
        school_list = School.objects.all()
    if category == "year":
        big = int(specific)
        cat = str(specific)
        big_human = humans.filter(player__grad_year=big)
        big_zombie = zombies.filter(player__grad_year=big)
        meal_list = Meal.objects.filter(game=g).filter(Q(eaten__grad_year=big) | Q(eater__grad_year=big))
        dorm_list = Building.objects.filter(building_type="D")
        school_list = School.objects.all()

    years = []
    if category != "year":
        for y in range(2012, 2020):
            year_human = big_human.filter(player__grad_year=y).count()
            year_zombie = big_zombie.filter(player__grad_year=y).count()
            if year_human + year_zombie > 0:
                years.append({'year': str(y), 'humans': year_human, 'zombies': year_zombie})
    dorms = []
    if category != "dorm":
        for d in dorm_list:
            dorm_human = big_human.filter(player__dorm=d).count()
            dorm_zombie = big_zombie.filter(player__dorm=d).count()
            if dorm_human + dorm_zombie > 0:
                dorms.append({'name': str(d.name), 'humans': dorm_human, 'zombies': dorm_zombie, 'id': str(d.id)})
    schools = []
    if category != "school":
        for s in school_list:
            school_human = big_human.filter(player__school=s).count()
            school_zombie = big_zombie.filter(player__school=s).count()
            if school_human + school_zombie > 0:
                schools.append({'name': str(s), 'humans': school_human, 'zombies': school_zombie})

    human_list = []
    for p in big_human:
        udata = {}
        udata["user_name"] = p.player.user.username
        udata["first"] = p.player.user.first_name
        udata["last"] = p.player.user.last_name
        if p.upgrade:
            udata["class"] = p.upgrade
        human_list.append(udata)

    zombie_list = []
    for p in big_zombie:
        udata = {}
        udata["user_name"] = p.player.user.username
        udata["first"] = p.player.user.first_name
        udata["last"] = p.player.user.last_name
        udata["meals"] = p.get_meals(g)
        if p.upgrade:
            udata["class"] = p.upgrade
        zombie_list.append(udata)

    meals = []
    for m in meal_list:
        from types import *
        if big_zombie.filter(player=m.eater).count() == 1:
            f_eater = "<a href=' / player / user / " + str(m.eater.user.username) + "' class='hoverme home' > " + str(m.eater) + "</a>"
        else:
            f_eater = "<a href=' / player / user / " + str(m.eater.user.username) + "' class='hoverme visitor' > " + str(m.eater) + "</a>"

        if big_zombie.filter(player=m.eaten).count() == 1:
            f_eaten = "<a href=' / player / user / " + str(m.eaten.user.username) + "' class='hoverme home' > " + str(m.eaten) + "</a>"
        else:
            f_eaten = "<a href=' / player / user / " + str(m.eaten.user.username) + "' class='hoverme visitor' > " + str(m.eaten) + "</a>"

        loc = m.location
        if type(loc) == NoneType:
            f_location = ""
        elif category == "school":
            if loc.building_type == "D":
                if loc.campus == big:
                    f_location = "<a href=' / status / dorm / " + str(loc.id) + "' class='hoverme home' > " + str(loc) + "</a>"
                else:
                    f_location = "<a href=' / status / dorm / " + str(loc.id) + "' class='hoverme visitor' > " + str(loc) + "</a>"
            else:
                if loc.campus == big:
                    f_location = "<span class='home' > " + str(loc) + "</span> "
                else:
                    f_location = "<span class='visitor' > " + str(loc) + "</span> "
        elif category == "dorm":
            if loc.building_type == "D":
                if loc == big:
                    f_location = "<a href=' / status / dorm / " + str(loc.id) + "' class='hoverme home' > " + str(loc) + "</a>"
                else:
                    f_location = "<a href=' / status / dorm / " + str(loc.id) + "' class='hoverme visitor' > " + str(loc) + "</a>"
            else:
                f_location = "<span class='visitor' > " + str(loc) + "</span> "
        else:
            if loc.building_type == "D":
                f_location = "<a href=' / status / dorm / " + str(loc.id) + "' class='hoverme' > " + str(loc) + "</a>"
            else:
                f_location = "<span > " + str(loc) + "</span> "

        meals.append({
            'eater': f_eater,
            'eaten': f_eaten,
            'when': m.time.strftime(' % a %I: % M%p'),
            'where': f_location,
            'o_time': m.time.isoformat(' ')
        })

    return render_to_response('stats / stat_detail.html',
        {
            "user": ui,
            'category': cat,
            'humans': big_human.count(),
            'zombies': big_zombie.count(),
            'years': years,
            'dorms': dorms,
            'schools': schools,
            'human_list': human_list,
            'zombie_list': zombie_list,
            'meals': meals,
        },
        context_instance=RequestContext(request),
    )
