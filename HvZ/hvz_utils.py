from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from datetime import datetime,timedelta,time
from HvZ.models import *
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from random import randint
from django.views.decorators.cache import cache_page
from django.utils.html import strip_tags
from django.db import connection

def get_current_game():
	''' returns an instance of the most recent game
	'''
	return Game.get_current()

def get_user_info(request):
	""" returns a dictionary with the following items:
		user username
		user first name
		user's team
			whether user is hardcore
			whether user is a mod
		-add more here when needed
	"""
	from HvZ.views import anonymous_info
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
