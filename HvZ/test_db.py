from django.db import connection, reset_queries
from django.http import HttpRequest
from time import clock
from HvZ.models import Registration, User
from HvZ.views import *

me = User.objects.get(email="jthemphill@gmail.com")

req = HttpRequest()
req.user = me

humans = Registration.objects.filter(team="H")
zombies = Registration.objects.filter(team="Z")

def q():
    return len(connection.queries)

def qt():
    return sum([float(x['time']) for x in connection.queries])

def test(view):
    reset_queries()
    t0 = clock()
    view(req)
    print "Total time: %s" % (clock() - t0)
    print "Total queries: %d" % q()


def elapsed_hours(t, t0):
    """Return the number of elapsed hours between t and t0"""
    dt = t - t0
    return (dt.days * 24) + (dt.seconds // 3600)

def stats(request):
	"""Test optimizations here before sticking them into production!"""
	g = get_current_game()
	ui = get_user_info(request)
	all = Registration.objects.filter(game=g).select_related()
	humans = all.filter(team="H")
	zombies = all.filter(team="Z")

	all_schools = School.objects.all()

	school_scores = {}
	for s in all_schools:
	    school_scores[s] = {
		'name':s.name,
		'humans':0,
		'zombies':0
		}
	    
	for h in humans.select_related("player__school"):
	    school_scores[h.player.school]['humans'] += 1

	for z in zombies.select_related("player__school"):
	    school_scores[z.player.school]['zombies'] += 1

	schools = school_scores

        print "Schools: %d" % q()


        # We should do something better than this with our constants!
        y0 = 2012
        yf = 2020

        humans_per_year = [0] * (yf - y0)
        zombies_per_year = [0] * (yf - y0)

        for h in humans:
            if h.player.grad_year:
                i = h.player.grad_year - y0
                humans_per_year[i] += 1

        for z in zombies:
            if z.player.grad_year:
                i = z.player.grad_year - y0
                zombies_per_year[i] += 1

        years = [{"year": y,
                  "humans": humans_per_year[y-y0],
                  "zombies": zombies_per_year[y-y0]} for y in xrange(y0, yf)]

        print "Years: %d" % q()

	all_dorms = Building.objects.filter(building_type="D")
        scores = dorm_populations(all_dorms, humans, zombies)

	dorms = scores

        print "dorms: %d" % q()

	human_list = []
	for p in humans:
		udata = {}
		udata["user_name"] = p.player.user.username
		udata["first"] = p.player.user.first_name
		udata["last"] = p.player.user.last_name
		if p.upgrade:
			udata["class"] = p.upgrade
		human_list.append(udata)

        print "humans: %d" % q()

        meal_dict = all_meals(g, zombies)

	zombie_list = []
	for p in zombies.select_related("player__user"):
		udata = {}
		udata["user_name"] = p.player.user.username
		udata["first"] = p.player.user.first_name
		udata["last"] = p.player.user.last_name
		udata["meals"] = meal_dict[p.player]
		if p.upgrade:
			udata["class"] = p.upgrade
		zombie_list.append(udata)

        print "zombies: %d" % q()

        meal_db = Meal.objects.filter(game=g).select_related("location__name",
                                                             "location__campus",
                                                             "eater__user",
                                                             "eaten__user")

	meals = []
	for m in meal_db:
		f_eater = "<a href='/player/user/"+str(m.eater.user.username)+"' class='hoverme'>"+str(m.eater)+"</span>"
		f_eaten = "<a href='/player/user/"+str(m.eaten.user.username)+"' class='hoverme'>"+str(m.eaten)+"</span>"
		meals.append({
			'eater':f_eater,
			'eaten':f_eaten,
			'when':m.time.strftime('%a %I:%M%p'),
			'o_time':m.time.isoformat(' '),
			'location': str(m.location),
			'description': m.description,
			'timestamp':datetime.now()
		})

        print "meals: %d" % q()

	
	hum = Registration.objects.filter(game=g).count()-10   # 10 is the number of OZs  + mod listed as starting zed + press account
	zom = 10

        q0 = q()

	t0 = datetime.combine(g.start_date,time(8))
	dt = timedelta(hours=1)
        tf = datetime.now()

        num_hours = elapsed_hours(tf, t0) + 1

        # Initialize a list of buckets --- one for each hour
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

        print "Cost of meals per hour: %d" % (q() - q0)

        q0 = q()
        D = {
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
            }

        ci = RequestContext(request)

        t0 = clock()

        r = render_to_response('stat_home_fast.html', D, context_instance=ci)
        print "Cost to render page: %d" % (clock() - t0)

        return r

#print "Normal view..."
test(stats_home_view)

#print "Faster view..."
#test(stats)
