from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from datetime import datetime,timedelta,time
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from random import randint
from django.views.decorators.cache import cache_page
from django.utils.html import strip_tags
from django.db import connection

from HvZ.models import *
from HvZ.forms import EatForm, RegForm, PostForm, ResetForm, ThreadForm, LoginForm


def get_current_game():
	''' returns an instance of the most recent game
	'''
	g = Game.objects.order_by('-year','semester')[0]
	return g

def get_team(p):
	reg_list = Registration.objects.filter(game=get_current_game(),player=p)
	if reg_list.exists():
		return reg_list.get().team
	else:
		return "N"

def check_eat(eater,eaten,time=datetime.today()):
	g = get_current_game()
        errors = ""

	#is eater playing in this game
	eater_reg_list = Registration.objects.filter(player=eater,game=g)
	if eater_reg_list.exists():
	    eater_reg = eater_reg_list.get()
	else:
	    errors += "You have to be playing to eat someone!\n"

	#is eater a zombie
	if eater_reg.team=="Z":
	    print "The eater is a zombie, all is well\n"
	else:
	    errors += "Don't be a cannibal!\n"

	#is eaten playing in this game
	eaten_reg_list = Registration.objects.filter(player=eaten,game=g)
	if eaten_reg_list.exists():
	    eaten_reg = eaten_reg_list.get()
	else:
	    errors += "You can only eat the brains of people playing this game!\n"

	#is eaten a human
	if eaten_reg.team=="H":
	    print "The eaten is a human, all is well"
	else:
	    errors += "Eating zombie brains doesn't help!\n"

	#is eater also eaten
	if eaten_reg==eater_reg:
	    errors += "You can't eat yourself!\n"
	else:
	    print "You aren't eating yourself, all is well"

        #is meal in the future
	if time > datetime.today():
	    errors += "That time is in the future!\n"

        #does eater have too many bad attempts
        if eater.bad_meals > 9:
            errors = "You have attempted too many bad meals. Please see a moderator immediately."

	return errors

def eat(eater,eaten,time=datetime.today(),location=None,description=None):
        g = get_current_game()
        #double check to make sure meal is valid
        errors = check_eat(eater,eaten,time=datetime.today())

	if errors != "":
		eater.bad_meals += 1
	        eater.save()
		return errors
	#save the meal
	Meal(eater=eater,eaten=eaten,game=g,time=time,location=location,description=description).save()

	#turn eaten into zombie
	eaten_reg.team="Z"

	#change eaten's upgrade
	#if eaten_reg is not Null and eaten_reg.upgrade.size:
	#eaten_reg.upgrade = "Ex-"+eaten_reg.upgrade

	#save changes to eaten
	eaten_reg.save()

	#return all clear
	return "You have eaten "+str(eaten)+"!\n"

def anonymous_info():
	return {"username": "AnonymousUser",
		"firstname": "Player",
		"team": "N",
		"isMod": False,
		"hardcore": False}

def get_user_info(request):
	""" returns a dictionary with the following items:
	    user username
	    user first name
	    user's team
            whether user is hardcore
            whether user is a mod
	    -add more here when needed
        """
	if request.user.is_anonymous():
		return anonymous_info()

	u = request.user

	p = Player.objects.filter(user=u)
	if p.exists():
		p = p.get()
	else:
		return anonymous_info()

	g = get_current_game()
	reg_list = Registration.objects.filter(player=p, game=g)

	if reg_list.exists():
		# player is in game
		r = reg_list.get()
		return {"username": u.username,
                        "firstname": u.first_name,
                        "team": r.team,
                        "isMod": p.is_mod(),
                        "hardcore": r.hardcore,
                        "player": p,
                     }

	# player is not in game
	return {"username": u.username,
                "firstname": u.first_name,
                "team": "N",
                "isMod": False,
                "hardcore": False,
              }

def login_user(request):
	''' login view, call this if you want to log someone in '''
	state = "Please log in to the website:"
	username = password = ''
	if request.POST:
		username = request.POST.get('username').lower()
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			login(request,user)
			state = "You're successfully logged in!"
		else:
			state = "Your username and/or password were incorrect"
	return render_to_response('auth.html',
                                  {'state':state, 'username':username})

def forbidden(request):
	ui = get_user_info(request)
	return render_to_response('forbidden.html',
				  {"user":ui},
				  context_instance=RequestContext(request))

def get_on_duty():
	''' returns a dictionary with the following items:
	    name first name of the moderator currently on duty
	    cell cell number of the moderator currently on duty
	'''
	from datetime import datetime
	cur_time = datetime.now()
	od_object = OnDuty.objects.filter(start_time__lte=cur_time,end_time__gte=cur_time)
	if od_object.exists():
		mod = od_object.get().mod
		return {"name": str(mod), "cell": "+1%s" % mod.cell}
	else:
		return {"name": "apparently no one", "cell": "N/A"}

def clean_feed_code(inputString):
	replacements = [("B", "A"), ("H", "A"), ("G","C"), ("F","E"), ("I","L"), ("M","N"), ("D","O"), ("Q","O"), ("R","P"), ("J","T"), ("U","W"), ("V","W"), ("K","X"), ("Y","X")]
	output = inputString
	for old, new in replacements:
		output = output.replace(old, new)
	output = output.upper()
	return output


def log_user_in(request):
	"""Logs a user in if possible and returns a string
	representing the given user's status.
	"""
	username = request.POST['email'].lower()
	password = request.POST['password']
	user = authenticate(username=username, password=password)

	if not user:
		return "Bad username or password"

	if user.is_active:
		login(request, user)
		return "success"

	return "Inactive"

def login_view(request):
	if request.method == 'POST':
		f = LoginForm(request.POST)
		if f.is_valid():
			w = log_user_in(request)
		else:
			w = "Your errors are: "+str(f.is_valid())
		return render_to_response('logout.html',
			{
				"worked": w,
			},
			context_instance=RequestContext(request),
		)
	return render_to_response('login.html',
		{
			"form": LoginForm()
		},
		context_instance=RequestContext(request),
	)

def logout_view(request):
	from django.contrib.auth import logout
	if request.method == 'POST':
		logout(request)
	return render_to_response('logout.html',
		{
			"worked": request.method == 'POST'
		},
		context_instance=RequestContext(request),
	)

def twilio_call_view(request):
	od = get_on_duty()
	return render_to_response('call.xml',
		{"name":od["name"],
		 "cell":od["cell"]},
		context_instance=RequestContext(request),
		mimetype="text/xml")

def twilio_sms_view(request):
	from HvZ.models import Player, Registration, PlayerSetting, School, Meal, Game
	import re
	if request.GET.get("To",0)=="+19095254551":
		#received something from twilio
		msg = request.GET.get("Body","Help")
		cmd = msg.partition(" ")[0].lower()
		arg = msg.partition(" ")[2].lower()
		sender_pots = Player.objects.filter(cell=str(request.GET.get("From","+10"))[2:])
		if sender_pots.exists():
			sender_player = sender_pots.get()
			sender_team = get_team(sender_player)
			resp = "You have been identified as: "+str(sender_player)
			if True:
				sender_pots = Registration.objects.filter(player=sender_player,game=get_current_game())
				if sender_pots.exists():
					sender_reg = sender_pots.get()
					if cmd=="mod":
						od = get_on_duty()
						if arg=="":
							resp = "The on duty moderator is "+od["name"]+". You can reach them by calling this number."
					elif cmd=="stop" or cmd=="quit" or cmd=="unsubscribe" or cmd=="leave":
						sender_player.cell="";
						sender_player.save()
						resp = "You have been removed from all ZOMCOM and TacNet texting services. You are still playing the game. To sign up again, go to the website."
					elif cmd=="status":
						regs = Registration.objects.filter(game=get_current_game())
						H = regs.filter(team="H").count()
						Z = regs.filter(team="Z").count()
						if len(arg)==0:
							resp = "Humans: "+str(H)+" \nZombies: "+str(Z)
						elif School.objects.filter(name=arg).exists():
							hcount = str(H.filter(player__school__name=arg).count())
							zcount = str(Z.filter(player__school__name=arg).count())
							resp = str(School.objects.get(name=arg))+" has \nHumans: "+hcount+" \nZombies: "+zcount
						elif Building.objects.filter(name=arg).exists():
							hcount = str(H.filter(player__dorm__name=arg).count())
							zcount = str(Z.filter(player__dorm__name=arg).count())
							resp = str(Building.objects.get(name=arg))+" has \nHumans: "+hcount+" \nZombies: "+zcount
						elif re.match(r"\d{4}",arg)>-1:
							hcount = str(H.filter(player__grad_year=arg).count())
							zcount = str(Z.filter(player__grad_year=arg).count())
							resp = "Class of "+str(arg)+" has \nHumans: "+hcount+" \nZombies: "+zcount
						else:
							resp = "Please enter status with either a 4 digit year, the name of the school (Mudd, CMC, Pitzer, Pomona, Scripps, Keck, CGU, or None), dorm, or alone to find out human and zombie counts."
					elif cmd=="feed" or cmd=="eat":
						code = arg.partition(" ")[0].upper()
						desc = arg.partition(" ")[2]
						eaten_reg = Registration.objects.get(feed=clean_feed_code(code))
						resp = eat(eater=sender_player,eaten=eaten_reg.player,description=desc,time=datetime.now())
					elif cmd=="mission":
						missions = Mission.objects.filter(result="N").order_by('-day','-kind')
						if sender_team=="N":
							resp = "You can only get missions if you are in the current game."
						elif sender_team=="H":
							missions = missions.exclude(show_players="M").exclude(show_players="Z")
						else:
							missions = missions.exclude(show_players="M").exclude(show_players="H")

						if arg=="npc":
							missions = missions.filter(kind="X")
						elif arg=="legendary":
							missions = missions.filter(kind="Y")
						if missions.exists():
							m = missions[0]
							if sender_team=="H":
								resp = m.human_title+" ("+m.get_day()+" "+m.get_kind()+"): "+m.human_SMS
							else:
								resp = m.zombie_title+" ("+m.get_day()+" "+m.get_kind()+"): "+m.zombie_SMS
						else:
							resp = "No mission of that type is visible to you yet."
					elif cmd=="time":
						resp = datetime.now()
					else:
						resp="Valid commands are status, mod, mission, feed, stop, and help."
				else:
					resp="You are not registered for the current game."
			else:
				resp="You have sending commands disabled. Please go to the webite to enable this feature."
		elif "@" in cmd:
			sender = User.objects.filter(email__iexact=cmd)
			if sender.exists():
				player = Player.objects.get(user=sender.get())
				player.cell = str(request.GET.get("From","+10"))[2:]
				player.save()
				resp = "You have been added to ZOMCOM and TacNet."
			else:
				resp = "No one with that email address is registered for ClaremontHvZ."
		else:
			resp = "You are not signed up for ZOMCOM and TacNet. Please text the email address you used for this game to this number to join."
	else:
		resp = "You viewed this page manually, it should only be viewed by phones."
	return render_to_response('sms.xml',
		{"response":resp, "to_mod": False
		},
		context_instance=RequestContext(request),
		mimetype="text/xml")

def all_meals(g, zombies):
	"""Map each zombie to the number of meals he or she has eaten.

	This function is only used to limit the number of queries made
	to the database in player_user_search and will become
	unnecessary once the Player model contains a field with their
	number of meals or a has_many table to all of their meals.

	Keyword arguments:
	g: The current game.
	zombies: The list of all zombies.

	This function returns a dictionary.

	"""
	zombies = zombies.select_related("player")

	ret = {}
	for z in zombies:
		ret[z.player] = 0

	for m in Meal.objects.filter(game = g).select_related("eater"):
		if m.eater in ret:
			ret[m.eater] += 1

	return ret

@cache_page(60*5)
def player_user_search(request):
	''' if logged in, currently returns terrible table of all users, if not
	    logged in asks user to log in (theoretically) '''
	ui = get_user_info(request)
	if ui["team"] == 'N':
		return forbidden(request)
	g = get_current_game()
	registrations = Registration.objects.filter(game=g).select_related("player",
									   "player__user",
									   "player__school")
	zombies = registrations.filter(team="Z") # Only needed for all_meals

	# FIXME: Humans can have meals too!
	meals = all_meals(g, zombies)

	players = []
	for r in registrations:
		p = r.player
		u = p.user
		temp = {}
		temp["username"] = u.username
		temp["first"] = u.first_name
		temp["last"] = u.last_name
		temp["school"] = str(p.school)
		temp["year"] = str(p.grad_year)
		temp["past"] = 0 #len(Registration.objects.filter(game__id__lt=g.id,player=p))
		temp["hardcore"] = r.hardcore
		if r.team=="H":
			temp["team"] = "Human"
			temp["meals"] = ""
		else:
			temp["team"] = "Zombie"
			temp["meals"] = meals[p]
		if r.upgrade:
			temp["class"] = r.upgrade
		players.append(temp)

	return render_to_response('user_search.html',
				  {"user": ui,
                               "players": players,
                              },
				  context_instance=RequestContext(request))


def player_user_profile(request, user_name):
	''' if logged in, returns a players profile, if not logged in asks user
	    to log in (theoretically)
        '''
	ui = get_user_info(request)
	if ui["team"] == 'N':
		return forbidden(request)
	g = get_current_game()
	user = User.objects.filter(username__iexact=user_name)[0]
	player = Player.objects.filter(user=user)[0]
	reg = Registration.objects.filter(player=player,game=g)[0]
	return render_to_response('profile.html',
				{
					"user": ui,
				  	"first":user.first_name,
					"last":user.last_name,
					"school":player.school,
					"grad_year":player.grad_year,
					"team": reg.team,
					"hardcore": reg.hardcore,
					"meals": reg.get_meals(g),
					"class": reg.upgrade,
					"feed": reg.feed,
					"isMe": user==request.user,
				},
				  context_instance=RequestContext(request))

@cache_page(60*5)
def homepage_view(request):
	ui = get_user_info(request)
	g = get_current_game()

	h_count = Registration.objects.filter(game=g,team="H").count()
	z_count = Registration.objects.filter(game=g,team="Z").count()

	if ui["team"] == 'N':
		return render_to_response('homepage.html',
			{
				"user": ui,
				"humans":h_count,
				"zombies": z_count,
				"onduty":get_on_duty(),
			},
			context_instance=RequestContext(request))
	else:
		team = ui["team"]
		missions = Mission.objects.filter(game=get_current_game(),result="N").exclude(show_players="M").exclude(kind="X").exclude(kind="Y")
		if team=="H":
			missions = missions.exclude(show_players="Z")
		else:
			missions = missions.exclude(show_players="H")

		if missions.exists():
			mission = missions.order_by('-day','-kind')[0]
		else:
			# This code is all kinds of placeholder! We're
			# returning a mission that happens to not be
			# over yet. What we really need is a dummy
			# mission to return.
			mission = Mission.objects.filter(result!="N")[0]

		m = dict()
		m["title"] = mission.get_title(team)
		m["day"] = mission.get_day()
		m["kind"] = mission.get_kind()
		m["story"] = mission.get_story(team)
		m["reward"] = mission.get_reward(team)
		if team=="H":
			m["goals"] = mission.human_goals
			m["rules"] = mission.human_rules
		else:
			m["goals"] = mission.zombie_goals
			m["rules"] = mission.zombie_rules

		return render_to_response('homepage.html',
			{
				"user": ui,
				"mission":m,
				"humans":h_count,
				"zombies": z_count,
				"onduty":get_on_duty(),
			},
			context_instance=RequestContext(request))

@cache_page(60*5)
def mission_list_view(request):
	ui = get_user_info(request)
	if ui["team"] == 'N':
		return forbidden(request)

	team = ui["team"]
	if team=="H":
		missions = Mission.objects.filter(game=get_current_game()).exclude(show_players="M").exclude(show_players="Z")
	else:
		missions = Mission.objects.filter(game=get_current_game()).exclude(show_players="M").exclude(show_players="H")
	if ui["hardcore"] == False:
		missions = missions.exclude(kind="Y")

	ml = []
	for m in missions:
		p_day = m.get_day()[:3]
		p_kind = m.get_kind()
		p_result = m.get_result()
		o_result = m.get_result_order()

		ml.append({'id':m.id, 'title':m.get_title(ui["team"]), 'day':m.day, 'p_day':p_day, 'kind':m.kind, 'p_kind':p_kind, 'result':o_result, 'p_result':p_result})
	return render_to_response('mission.html',
		{
			'mission_list':ml,
			"user": ui,
		},
		context_instance=RequestContext(request))

@cache_page(60*5)
def mission_json_view(request,mission_id):
	import json
	ui = get_user_info(request)
	if ui["team"] == 'N':
		return forbidden(request)

	team = ui["team"]

	m = Mission.objects.get(id=mission_id)
	details = dict()
	details["title"] = m.get_title(team)
	details["day"] = m.get_day()
	details["kind"] = m.get_kind()
	details["result"] = m.get_result()

	details["story"] = m.get_story(team)
	details["reward"] = m.get_reward(team)
	if team=="Z":
		details["rules"] = m.zombie_rules
		details["goals"] = m.zombie_goals
	else:
		details["rules"] = m.human_rules
		details["goals"] = m.human_goals

	return render_to_response('mission.json',
		{'json':json.dumps(details,indent=4),
		},
		context_instance=RequestContext(request),
		mimetype="application/json")

def elapsed_hours(t, t0):
    """Return the number of elapsed hours between t and t0"""
    dt = t - t0
    return (dt.days * 24) + (dt.seconds // 3600)

def old_histograms(g):
	"""Generate two dictionaries used to display the cumulative and meal density graphs.

	This function is deprecated by meal_histograms, which does not
	make one db query for every hour since game start.

	"""
	per_hour = []
	upto_hour = []

	start_time = datetime.combine(g.start_date,time(8))
	end_time = datetime.combit(g.start_date,time(21))+timedelta(days=4)
	hum = Registration.objects.filter(game=g).count()-10
	zom = 10
	end_add = timedelta(hours=1)
	while start_time < datetime.today() and start_time < end_time: # One query for every hour
		meals_in_hour = Meal.objects.filter(game=g,
						    time__gte=start_time,
						    time__lt=start_time+end_add).count()
		per_hour.append({"hour": start_time, "meals": meals_in_hour})
		hum -= meals_in_hour
		zom += meals_in_hour
		upto_hour.append({"hour": start_time+end_add, "humans": hum, "zombies": zom})
		start_time += end_add
	return per_hour, upto_hour


def meal_histograms(g):
	"""Generate two dictionaries used to display the cumulative and meal density graphs."""
	# 10 is the number of OZs + mod listed as starting zed + press
	# account
	hum = Registration.objects.filter(game=g).count()-10
	zom = 10

	t0 = datetime.combine(g.start_date,time(8))
	dt = timedelta(hours=1)

	"""tf is the earlier of now or the game's end time"""
	end = datetime.combine(g.start_date,time(21))+timedelta(days=4)
	tf = datetime.now()
	if end < tf:
		tf = end

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

	return (per_hour, upto_hour)

def get_stat(game, constraints):
	# We're not using a QuerySet because they don't support joins (not that I could find, anyway).
	# This could (should) be improved by using 'group by' for sets of stats. That will take some
	# annoying reformatting to be useful, though.
	baseQuery = "select count(*) from HvZ_registration, HvZ_player where HvZ_player.id=player_id and HvZ_registration.game_id="
	# Yes, I know you're thinking 'Security risk!!', but all strings passed to getStat will be hardcoded SQL
	# or autogenerated id's, so there shouldn't be any injection opportunities.
	query = baseQuery + str(game.id)
	while len(constraints) != 0:
		query += ' and ' + constraints.pop()

	cursor = connection.cursor()
	cursor.execute(query)
	results = cursor.fetchall()
	return int(results[0][0])

def school_team_counts(game):
	"""Get the number of humans and zombies per school."""
	all_schools = School.objects.all()

        school_scores = {}
        for s in all_schools:
		school_scores[s] = {
			'name':s.name,
			'humans': get_stat(game, ["team='H'", "school_id="+str(s.id)]) ,
			'zombies': get_stat(game, ["team='Z'", "school_id="+str(s.id)])
			}
	return school_scores.values()

def year_team_counts(humans, zombies, game):
	"""Get the number of humans and zombies per year."""
	# We should do something better than this with our constants!
	# For some reason, this function used to return nonzero graduates for 2019. That's been fixed.
	y0 = 2012
	yf = 2020
	return [{"year": y,
		  "humans": get_stat(game, ["team='H'", "grad_year="+str(y)]),
		  "zombies": get_stat(game, ["team='Z'", "grad_year="+str(y)])} for y in xrange(y0, yf)]

def stats_home_view(request):
	return stats_home(request, "stats/stat_home.html")

def stats_home_fast(request):
	return stats_home(request, "stats/stat_home_fast.html")

def stats_home(request, template):
	g = get_current_game()
	ui = get_user_info(request)
	all = Registration.objects.filter(game=g).select_related()
	humans = all.filter(team="H")
	zombies = all.filter(team="Z")

	schools = school_team_counts(g)

	years = year_team_counts(humans, zombies, g)

	all_dorms = Building.objects.filter(building_type="D")
	dorms = dorm_populations(all_dorms, humans, zombies)

	human_list = []
	for p in humans:
		udata = {}
		udata["user_name"] = p.player.user.username
		udata["first"] = p.player.user.first_name
		udata["last"] = p.player.user.last_name
		if p.upgrade:
			udata["class"] = p.upgrade
		human_list.append(udata)

	# FIXME: Humans can have meals too!
	meal_counts = all_meals(g, zombies)

	zombie_list = []
	for p in zombies:
		udata = {}
		udata["user_name"] = p.player.user.username
		udata["first"] = p.player.user.first_name
		udata["last"] = p.player.user.last_name
		udata["meals"] = meal_counts[p.player]
		if p.upgrade:
			udata["class"] = p.upgrade
		zombie_list.append(udata)

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


	per_hour, upto_hour = meal_histograms(g)

	return render_to_response(template,
		{
			"user": ui,
			'humans':humans.count(),
			'zombies':zombies.count(),
			'schools':schools,
			'years':years,
			'dorms':dorms,
			'meals':meals,
			'mph': per_hour,
			'mun': upto_hour,
			'human_list':human_list,
			'zombie_list':zombie_list,
		},
		context_instance=RequestContext(request))

def dorm_populations(dorms, humans, zombies):
    scores = {}
    for d in dorms.select_related("campus"):
        scores[d] = {
		'name':str(d),
		'id':str(d.id),
		'humans': 0,
		'zombies': 0
		}

    for h in humans.select_related("player__dorm"):
        d = h.player.dorm
        if d in scores:
            scores[d]['humans'] += 1

    for z in zombies.select_related("player__dorm"):
        d = z.player.dorm
        if d in scores:
            scores[d]['zombies'] += 1

    return scores.values()

@cache_page(60*5)
def stats_category_view(request,category):
	g = get_current_game()
	ui = get_user_info(request)
	all = Registration.objects.filter(game=g)
	data = []
	if category=="school":
		for s in School.objects.all().order_by("name"):
			school_human = all.filter(player__school=s,team="H").count()
			school_zombie = all.filter(player__school=s,team="Z").count()
			if school_human + school_zombie > 0:
				data.append({'id': s.id, 'name': str(s), 'humans':school_human, 'zombies':school_zombie})
	elif category=="dorm":
		for d in Building.objects.filter(building_type="D").order_by("name"):
			dorm_human = all.filter(player__dorm=d,team="H").count()
			dorm_zombie = all.filter(player__dorm=d,team="Z").count()
			if dorm_human + dorm_zombie > 0:
				data.append({'id': d.id, 'name': str(d), 'humans':dorm_human, 'zombies':dorm_zombie})
	elif category=="year":
		for y in range(2011,2020):
			year_human = all.filter(player__grad_year=y,team="H").count()
			year_zombie = all.filter(player__grad_year=y,team="Z").count()
			if year_human + year_zombie > 0:
				data.append({'id': y, 'name': str(y), 'humans':year_human, 'zombies':year_zombie})
	elif category=="human" or category=="zombie":
		if category=="human":
			players = all.filter(team="H")
		else:
			players = all.filter(team="Z")

		school = []
		for s in School.objects.all().order_by("name"):
			count = players.filter(player__school=s).count()
			if count > 0:
				school.append({'name': str(s), 'members':count})

		dorm = []
		for d in Building.objects.filter(building_type="D").order_by("name"):
			count = players.filter(player__dorm=d).count()
			if count > 0:
				dorm.append({'name': str(d), 'members':count})

		year = []
		for y in range(2011,2020):
			count = players.filter(player__grad_year=y).count()
			if count > 0:
				year.append({'name': str(y), 'members':count})

		player_list = []
		for r in players:
			pdata = dict()
			pdata['first'] = r.player.user.first_name
			pdata['last'] = r.player.user.last_name
			pdata['school'] = r.player.school
			pdata['year'] = r.player.grad_year
			pdata['class'] = r.upgrade
			if category=="zombie":
				pdata["meals"] = r.get_meals(g)
			else:
				pdata["hardcore"] = r.hardcore
			player_list.append(pdata)

	if category in ["school","dorm","year"]:
		return render_to_response('stats/stat_category.html',
			{
				"user":ui,
				'data':data,
			},
			context_instance=RequestContext(request))
	else:
		return render_to_response('stats/stat_team.html',
			{
				"user":ui,
				'category':category,
				'schools':school,
				'years':year,
				'dorms':dorm,
				'player_list':player_list,
			},
			context_instance=RequestContext(request))

@cache_page(60*5)
def stats_detail_view(request,category,specific):
	ui = get_user_info(request)
	from django.db.models import Q
	g = get_current_game()
	ui = get_user_info(request)
	all = Registration.objects.filter(game=g)
	humans = all.filter(team="H")
	zombies = all.filter(team="Z")

	data = []
	if category=="school":
		big = School.objects.filter(name=specific)[0]
		cat = big.name
		big_human = humans.filter(player__school=big)
		big_zombie = zombies.filter(player__school=big)
		meal_list = Meal.objects.filter(game=g).filter( Q(eaten__school=big) | Q(eater__school=big) | Q(location__campus=big) )
		dorm_list = Building.objects.filter(building_type="D").filter(Q(campus=big) | Q(campus=None))
	if category=="dorm":
		big = Building.objects.filter(id=specific)[0]
		cat = big.name
		big_human = humans.filter(player__dorm=big)
		big_zombie = zombies.filter(player__dorm=big)
		meal_list = Meal.objects.filter(game=g).filter(Q(eaten__dorm=big) | Q(eater__dorm=big) | Q(location=big))
		school_list = School.objects.all()
	if category=="year":
		big = int(specific)
		cat = str(specific)
		big_human = humans.filter(player__grad_year=big)
		big_zombie = zombies.filter(player__grad_year=big)
		meal_list = Meal.objects.filter(game=g).filter(Q(eaten__grad_year=big) | Q(eater__grad_year=big))
		dorm_list = Building.objects.filter(building_type="D")
		school_list = School.objects.all()

	years = []
	if category != "year":
		for y in range(2012,2020):
			year_human = big_human.filter(player__grad_year=y).count()
			year_zombie = big_zombie.filter(player__grad_year=y).count()
			if year_human + year_zombie > 0:
				years.append({'year':str(y), 'humans':year_human, 'zombies':year_zombie})
	dorms = []
	if category != "dorm":
		for d in dorm_list:
			dorm_human = big_human.filter(player__dorm=d).count()
			dorm_zombie = big_zombie.filter(player__dorm=d).count()
			if dorm_human + dorm_zombie > 0:
				dorms.append({'name': str(d.name), 'humans':dorm_human, 'zombies':dorm_zombie, 'id':str(d.id)})
	schools = []
	if category != "school":
		for s in school_list:
			school_human = big_human.filter(player__school=s).count()
			school_zombie = big_zombie.filter(player__school=s).count()
			if school_human + school_zombie > 0:
				schools.append({'name': str(s), 'humans':school_human, 'zombies':school_zombie})

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
		if big_zombie.filter(player=m.eater).count()==1:
			f_eater = "<a href='/player/user/"+str(m.eater.user.username)+"' class='hoverme home'>"+str(m.eater)+"</a>"
		else:
			f_eater = "<a href='/player/user/"+str(m.eater.user.username)+"' class='hoverme visitor'>"+str(m.eater)+"</a>"

		if big_zombie.filter(player=m.eaten).count()==1:
			f_eaten = "<a href='/player/user/"+str(m.eaten.user.username)+"' class='hoverme home'>"+str(m.eaten)+"</a>"
		else:
			f_eaten = "<a href='/player/user/"+str(m.eaten.user.username)+"' class='hoverme visitor'>"+str(m.eaten)+"</a>"


		loc = m.location
		if type(loc) == NoneType:
			f_location = ""
		elif category=="school":
			if loc.building_type=="D":
				if loc.campus==big:
					f_location = "<a href='/status/dorm/"+str(loc.id)+"' class='hoverme home'>"+str(loc)+"</a>"
				else:
					f_location = "<a href='/status/dorm/"+str(loc.id)+"' class='hoverme visitor'>"+str(loc)+"</a>"
			else:
				if loc.campus==big:
					f_location = "<span class='home'>"+str(loc)+"</span>"
				else:
					f_location = "<span class='visitor'>"+str(loc)+"</span>"
		elif category=="dorm":
			if loc.building_type=="D":
				if loc==big:
					f_location = "<a href='/status/dorm/"+str(loc.id)+"' class='hoverme home'>"+str(loc)+"</a>"
				else:
					f_location = "<a href='/status/dorm/"+str(loc.id)+"' class='hoverme visitor'>"+str(loc)+"</a>"
			else:
				f_location = "<span class='visitor'>"+str(loc)+"</span>"
		else:
			if loc.building_type=="D":
				f_location = "<a href='/status/dorm/"+str(loc.id)+"' class='hoverme'>"+str(loc)+"</a>"
			else:
				f_location = "<span>"+str(loc)+"</span>"

		meals.append({
			'eater':f_eater,
			'eaten':f_eaten,
			'when':m.time.strftime('%a %I:%M%p'),
			'where':f_location,
			'o_time':m.time.isoformat(' ')
		})

	return render_to_response('stats/stat_detail.html',
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
			'meals':meals,
		},
		context_instance=RequestContext(request),
	)

@cache_page(60*5)
def rules_list_view(request):
	rule_list = Rule.objects
	ui = get_user_info(request)
	basics= []
	for r in rule_list.filter(category="B").order_by('-priority'):
		basics.append({"id": r.id, "title":r.title, "description":r.description})

	classes = []
	for r in rule_list.filter(category="C").order_by('-priority'):
		classes.append({"id": r.id, "title":r.title, "description":r.description, "pic":r.image})

	return render_to_response('rules.html',
		{
			"user":ui,
			"basics": basics,
			"classes": classes,
			"locations": [],
		},
		context_instance=RequestContext(request),
	)

@cache_page(60*5)
def rules_json_view(request,rule_type,rule_id):
    import json
    from django.core.exceptions import MultipleObjectsReturned
    from django.core.exceptions import ObjectDoesNotExist
    import sys
    if rule_type == "l":
        loc = Building.objects.get(id=rule_id)
        # Give blank defaults in case rule does not exist
        details = {"lat":float(loc.lat), "lng":float(loc.lng), "pic":"",
                   "youtube": "", "details": ""}
        # Search for the associated rule
        try:
            r = None  # Set to None first in case of MultipleObjectsReturned
            r = Rule.objects.get(location=rule_id)
        # If there are too many objects, there is something broken in the
        # database. Shout a warning, then return the first one found
        except MultipleObjectsReturned:
            print "Multiple Rules for location: " + loc.name + "."
            rGroup = Rule.objects.filter(location=rule_id)
            r = rGroup[0] # Set to first rule found
        #except ObjectDoesNotExist: # If there was no object, we don't care
        finally:
            # If there was an object, add to dictionary
            if (r != None):
                details["image"] = str(r.image)
                details["youtube"] = r.youtube
                details["details"] = r.examples
    else:
		r = Rule.objects.get(id=rule_id)
		details = ({"details": r.examples, "youtube": r.youtube, "image":str(r.image)})
    return render_to_response('mission.json',
        {'json':json.dumps(details,indent=4),
        },
        context_instance=RequestContext(request),
        mimetype="application/json",
    )

def eat_view(request):
	ui = get_user_info(request)
	g = get_current_game()
	if ui["team"] != 'Z':
		return forbidden(request)
	if request.method == 'POST':
		form = EatForm(request.POST)
		if form.is_valid():
			clean_fc = clean_feed_code(form.cleaned_data['feed_code'])
			eaten_reg_list = Registration.objects.filter(game=get_current_game,feed=clean_fc)
			if eaten_reg_list.exists():
				eaten_reg = eaten_reg_list.get()
				eaten = eaten_reg.player
				eater = Player.objects.get(user=request.user)

				mealtime = datetime.combine(g.start_date,time.min)+timedelta(days=int(form.cleaned_data['meal_day'])-1,hours=int(form.cleaned_data['meal_hour'])+12*int(form.cleaned_data['meal_ap']),minutes=int(form.cleaned_data['meal_mins']))
				eat_check = eat(eater=eater,eaten=eaten,time=mealtime,description=form.cleaned_data['description'],location=form.cleaned_data['location'])
				if "You have eaten" in eat_check:
					form = EatForm()
				return render_to_response('eat.html',
					{
						"user": ui,
						"preform": eat_check.split("\n")[:-1],
						"form": form,
					},
					context_instance=RequestContext(request),
				)
			else:
				eater = Player.objects.get(user=request.user)
				eater.bad_meals += 1
				eater.save()
				return render_to_response('eat.html',
					{
						"user": ui,
						"preform": ["No one with that feed code exists."],
						"form": form,
					},
					context_instance=RequestContext(request),
				)

	else:
		form = EatForm()
	return render_to_response('eat.html',
		{
			"user": ui,
			"form": form,
		},
		context_instance=RequestContext(request),
	)

def register_view(request):
	if request.method == 'POST':
		form = RegForm(request.POST)
		if form.is_valid():
			clean_fc = clean_feed_code(form.cleaned_data['feed'])
			if User.objects.filter(email__iexact=form.cleaned_data['email']).exists():
				u = User.objects.filter(email__iexact=form.cleaned_data['email'])[0]
				u2 = User.objects.filter(first_name=form.cleaned_data['first'], last_name=form.cleaned_data['last'], password="potato")
				if u.password=="potato" or u2.exists():
					if u2.exists():
						u = u2.get()
						u.email=form.cleaned_data['email']
						u.username=form.cleaned_data['email']
					u.first_name=form.cleaned_data['first']
					u.last_name=form.cleaned_data['last']
					u.set_password(form.cleaned_data['password'])
					u.save()
					p = Player.objects.get(user=u)
					p.school=form.cleaned_data['school']
					p.dorm=form.cleaned_data['dorm']
					p.grad_year=form.cleaned_data['grad']
					p.cell=form.cleaned_data['cell']
					p.save()
					if len(Registration.objects.filter(player=p,game=get_current_game()))==0:
						r = Registration(player=p,game=get_current_game(),team="H",feed=clean_fc,hardcore=form.cleaned_data['hardcore'])
						if form.cleaned_data['oz'] and form.cleaned_data['c3']:
							r.upgrade = "OZ Pool - C3 Pool"
						elif form.cleaned_data['oz']:
							r.upgrade="OZ Pool"
						elif form.cleaned_data['c3']:
							r.upgrade = "C3 Pool"
						r.save()
						preform = "Welcome to another game, "+str(u.first_name)+" "+str(u.last_name)+"!"
					else:
						preform = "You are already registered for this game"
					form=RegForm()
				else:
					preform = "Someone with that email address already exists"
			else:
					u = User.objects.create_user(form.cleaned_data['email'],form.cleaned_data['email'],form.cleaned_data['password'])
					u.first_name=form.cleaned_data['first']
					u.last_name=form.cleaned_data['last']
					u.save()
					p = Player(user=u,school=form.cleaned_data['school'],dorm=form.cleaned_data['dorm'],grad_year=form.cleaned_data['grad'],cell=form.cleaned_data['cell'])
					p.save()
					r = Registration(player=p,game=get_current_game(),team="H",feed=clean_fc,hardcore=form.cleaned_data['hardcore'])
					if form.cleaned_data['oz']:
						r.upgrade="OZ Pool"
					r.save()
					preform = "Welcome to the game, "+str(u.first_name)+" "+str(u.last_name)+"!"
					form = RegForm()
		else:
			preform= "Something went wrong in your registration."
	else:
		form = RegForm()
		preform = ""
	return render_to_response('register.html',
		{
			"preform": preform,
			"form":form,
		},
		context_instance=RequestContext(request),
	)

@cache_page(60*5)
def plot_view(request):
	from django.db.models import Q

	ui = get_user_info(request)
	if ui["team"] == 'N':
		return forbidden(request)

	g = get_current_game()

	plot = dict()
	plot["Monday"] = []
	plot["Tuesday"] = []
	plot["Wednesday"] = []
	plot["Thursday"] = []
	plot["Friday"] = []
	plot["Saturday"] = []
	plot["Sunday"] = []

	mission = dict()
	mission["Monday"] = []
	mission["Tuesday"] = []
	mission["Wednesday"] = []
	mission["Thursday"] = []
	mission["Friday"] = []
	mission["Saturday"] = []
	mission["Sunday"] = []

	meal = dict()
	meal["Monday"] = []
	meal["Tuesday"] = []
	meal["Wednesday"] = []
	meal["Thursday"] = []
	meal["Friday"] = []
	meal["Saturday"] = []
	meal["Sunday"] = []


	for m in Mission.objects.filter(game=g).filter(Q(show_players="B") | Q(show_players=ui["team"])):
		mission[m.get_day()].append({"title":m.get_title(ui["team"]), "story":m.get_story(ui["team"])})

	for p in Plot.objects.filter(game=g).filter(reveal_time__lte=datetime.now()).filter(Q(show_side="B") | Q(show_side=ui["team"])):
		plot[p.reveal_time.strftime('%A')].append({"title":p.title, "story":p.story})

	for m in Meal.objects.filter(game=g).filter(description__contains=" "):
		meal[m.time.strftime('%A')].append({"title":str(m.eater)+" ate "+str(m.eaten), "story":m.description})

	days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	stories = []
	for d in days:
		stories.append({
			"day": d,
			"missions": mission[d],
			"plot": plot[d],
			"meals":meal[d],
		})

	return render_to_response('plot.html',
		{
			"user": ui,
			"days":days,
			"stories":stories,
		},
		context_instance=RequestContext(request),
	)

def mobile_eat_view(request,FeedCode=""):
	ui = get_user_info(request)
	g = get_current_game()
	if request.method == 'POST':
		if ui["username"] == "AnonymousUser":
			l_form = LoginForm(request.POST)
			if l_form.is_valid():
				#process login
				username = request.POST['email'].lower()
				password = request.POST['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						preform = "Logged in as "+str(user)
					else:
						#return inactive
						preform = "You are not signed up for this game"
						return render_to_response('mobileeat.html',
							{
								"user": ui,
								"login":LoginForm(initial={"email":username}),
								"result":[preform],
								"eat":EatForm(initial={"feed_code":FeedCode}),
							},
							context_instance=RequestContext(request),
						)
				else:
					#return bad login form
					preform = "You have entered an incorrect email address or password."
					return render_to_response('mobileeat.html',
						{
							"user": ui,
							"login":LoginForm(initial={"email":username}),
							"result":[preform],
							"eat":EatForm(initial={"feed_code":FeedCode}),
						},
						context_instance=RequestContext(request),
					)
			else:
				#return invalid login form
				preform = "You did not enter either your email address or password."
				return render_to_response('mobileeat.html',
					{
						"user": ui,
						"login":LoginForm(initial={"email":request.POST['email'].lower()}),
						"result":[preform],
						"eat":EatForm(initial={"feed_code":FeedCode}),
					},
					context_instance=RequestContext(request),
				)

		#process meal
		e_form = EatForm(request.POST)
		if e_form.is_valid():
			clean_fc = clean_feed_code(e_form.cleaned_data['feed_code'])
			eaten_reg_list = Registration.objects.filter(game=get_current_game,feed=clean_fc)
			if eaten_reg_list:
				eaten_reg = eaten_reg_list.get()
				eaten = eaten_reg.player
				eater = Player.objects.get(user=request.user)

				mealtime = datetime.combine(g.start_date,time.min)+timedelta(days=int(e_form.cleaned_data['meal_day'])-1,hours=int(e_form.cleaned_data['meal_hour'])+12*int(e_form.cleaned_data['meal_ap']),minutes=int(e_form.cleaned_data['meal_mins']))
				eat_check = eat(eater=eater,eaten=eaten,time=mealtime,description=e_form.cleaned_data['description'],location=e_form.cleaned_data['location'])
			else:
				eat_check = "You have entered an invalid feed code.\n"
			return render_to_response('mobileeat.html',
				{
					"user": ui,
					"login":"",
					"result": eat_check.split("\n")[:-1],
					"eat": EatForm(),
				},
				context_instance=RequestContext(request),
			)
		else:
			#return invalid eat form
			return render_to_response('mobileeat.html',
				{
					"user": ui,
					"login":"",
					"result": ["You did not enter a feed code."],
					"eat": EatForm(),
				},
				context_instance=RequestContext(request),
			)

	else:
		#display empty forms
		if ui["username"] == "AnonymousUser":
			l_form = LoginForm()
		else:
			l_form = ""
		e_form = EatForm(initial={"feed_code":FeedCode})
		preform=""
		return render_to_response('mobileeat.html',
			{
				"user": ui,
				"login":l_form,
				"result":preform,
				"eat":e_form,
			},
			context_instance=RequestContext(request),
		)

def forum_thread_view(request):
	ui = get_user_info(request)
	if ui["team"] == 'N':
		return forbidden(request)

	g = get_current_game()
	threads = ForumThread.objects.filter(game=g)

	bt = []
	tt = []
	for t in threads:
		n = dict()
		n["id"] = t.id
		n["title"] = t.title
		n["description"] = t.description
		n["created"] = t.create_time
		n["replies"] = t.post_count()
		if n["replies"]>0:
			lp = t.last_post()
			n["modified"] = lp.create_time
			n["last_poster"] = lp.creator
		else:
			n["modified"] = t.create_time
			n["last_poster"] = t.creator
		n["author"] = t.creator
		if t.visibility=="B":
			bt.append(n)
		elif t.visibility==ui["team"]:
			tt.append(n)

	return render_to_response('forum_thread.html',
			{
				"user": ui,
				"both_thread":bt,
				"team_thread":tt,
				"new":ThreadForm(),
			},
			context_instance=RequestContext(request),
		)

def format_slightly(text):
	"""Make the forum thread descriptions less wall of text-y.

	This will only work if the entire description has been wrapped
	in <p> tags!

	"""
	text = strip_tags(text)
	text.replace("\n\n", "</p><p>")
	text.replace("\n", "<br>")
	return text

def forum_post_view(request,Parent):
	cont = ForumThread.objects.get(id=Parent)
	posts = ForumPost.objects.filter(parent=cont).order_by('create_time')
	thread = []
	for p in posts:
		n = dict()
		n["poster_id"] = p.creator.user.username
		n["poster_name"] = str(p.creator)
		n["created"] = p.create_time
		n["contents"] = p.contents
		thread.append(n)

	if cont.visibility=="B":
		vis = "Both Teams"
	else:
		vis = "My Team"

	return render_to_response('forum_post.html',
			{
				"title": cont.title,
				"created":cont.create_time,
				"creator":cont.creator,
				"team":vis,
				"posts":thread,
				"description": cont.description,
				"reply":PostForm(initial={"parent":Parent}),
			},
			context_instance=RequestContext(request),
		)

def forum_new_post_view(request):
	ui = get_user_info(request)
	if request.method=="POST":
		post = PostForm(request.POST)
		if post.is_valid():
			#receiving parent and contents
			nfp = ForumPost(parent = ForumThread.objects.get(id=post.cleaned_data["parent"]), contents = post.cleaned_data["contents"], creator = ui["player"])
			try:
				nfp.save()
				return render_to_response('logout.html',
					{
						"worked":"worked",
					},
					context_instance=RequestContext(request),
				)
			except Exception:
				#return failure
				print "Form has values that couldn't be inserted"
		else:
			#return failure
			print "Form has invalid values"
	else:
		return render_to_response('mission.json')

def forum_new_thread_view(request):
	ui = get_user_info(request)
	g = get_current_game()
	if request.method=="POST":
		thread  = ThreadForm(request.POST)
		if thread.is_valid():
			#receiving title, description
			if thread.cleaned_data["visibility"] == "B":
				vis = "B"
			else:
				vis = ui["team"]
			ntp = ForumThread(title = thread.cleaned_data["title"], description = thread.cleaned_data["description"], visibility = vis, game = g, creator = ui["player"])
			try:
				ntp.save()
				return render_to_response('logout.html',
					{
						"worked":"worked",
					},
					context_instance=RequestContext(request),
				)
			except Exception:
				#return failure
				return render_to_response('logout.html',
					{
						"worked":thread,
					},
					context_instance=RequestContext(request),
				)
		else:
			#return failure
				return render_to_response('logout.html',
					{
						"worked":thread,
					},
					context_instance=RequestContext(request),
				)
	else:
		return render_to_response('logout.html',
			{
				"worked":"You didn't even POST anything.",
			},
			context_instance=RequestContext(request),
		)

def email_view(request):
	ui = get_user_info(request)
	g = get_current_game()
	if ui["isMod"]:
		humans = Registration.objects.filter(game=g,team="H")
		zombies = Registration.objects.filter(game=g,team="Z")
		return render_to_response("email.html",{
				"user": ui,
				"humans": humans,
				"zombies": zombies,
			},
			context_instance=RequestContext(request),
		)
	else:
		return forbidden(request)

def attendance_view(request):
	ui = get_user_info(request)
	g = get_current_game()
	day_list = [1,2,3,4]
	nb_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
	if ui["isMod"]:
		players = Registration.objects.filter(game=g).order_by('player__user__last_name','player__user__first_name')
		return render_to_response("here.html",{
				"dl": day_list,
				"nl": nb_list,
				"players": players,
			},
			context_instance=RequestContext(request),
		)
	else:
		return forbidden(request)

def duplicate_view(request):
	g = get_current_game()
	all = User.objects.all()
	dups = []
	for parent in all:
		check = User.objects.all()
		for child in check:
			if parent.last_name.lower() == child.last_name.lower() and parent.id < child.id:
				if Player.objects.filter(user=parent).exists() and Player.objects.filter(user=child).exists():
					parent_player = Player.objects.get(user=parent)
					child_player = Player.objects.get(user=child)
					if parent_player.school == child_player.school:
						left_regs = Registration.objects.filter(player__user=child)
						right_regs = Registration.objects.filter(player__user=parent)
						if len(left_regs)<2 and len(right_regs)<2:
							dups.append({"left": child, "left_in": left_regs, "right": parent, "right_in": right_regs})
	return render_to_response("duplicates.html",{
				"dups": dups,
			},
			context_instance=RequestContext(request),
		)

def not_registered_view(request):
	g = get_current_game()
	lg = Game.objects.filter(semester="F").get()
	ui = get_user_info(request)
	all = Player.objects.filter(grad_year=2015)
	humans = []
	zombies = []
	for p in all:
		if Registration.objects.filter(game=lg,player=p).exists() and not Registration.objects.filter(game=g,player=p).exists():
			humans.append({"player":p})
		elif Registration.objects.filter(game=g,player=p).exists() and not Registration.objects.filter(game=lg,player=p).exists():
			zombies.append({"player":p})
	return render_to_response("email.html",{
			"user": ui,
			"humans": humans,
			"zombies": zombies,
		},
		context_instance=RequestContext(request),
	)

def password_reset_view(request,hash=""):
	g = get_current_game()
	ui = get_user_info(request)
	rf = "";
	if request.method == "POST":
		target = User.objects.filter(username__iexact=request.POST['email'])
		if target.exists():
			fix = target.get()
			if "password" in request.POST:
				#they've typed in a new password
				err = "new password"
				if fix.password==request.POST['hash']:
					#the form the filled out is valid
					fix.set_password(request.POST['password'])
					fix.save()
					err = "Your password has been successfully reset to "+request.POST['password']
				else:
					err = "You are trying to hack into someone's account"
			else:
				#they are resetting their password
				temp = randint(100000,999999)
				fix.password = str(temp)
				fix.save()
				send_mail("Password Reset", "Your Password for Claremont HvZ has been erased. Please go to http://claremonthvz.org/player/passwordreset/"+str(temp)+"/ to enter a new password.", "web@claremonthvz.org", [fix.email], False)
				err = "success"
		else:
			err = "No one with that username exists."
		return render_to_response("logout.html",{
				"worked": err,
			},
			context_instance=RequestContext(request),
		)
	else:
		if hash!="":
			#Give them form for their email address and new password
			target = User.objects.filter(password=hash)
			if target.exists():
				err = "Fill out this form to reset your password."
				rf = ResetForm(initial={"hash":hash})
			else:
				err = "No one has that password reset code."
		else:
			err = "This is the password reset page"
	return render_to_response("password_reset.html",{
				"user":ui,
				"err": err,
				"rf": rf,
			},
			context_instance=RequestContext(request),
		)

def stats_down_view(request):
	ui = get_user_info(request)
	return render_to_response("stats_down.html",{
		"user":ui,
		},
		context_instance=RequestContext(request)
	)
