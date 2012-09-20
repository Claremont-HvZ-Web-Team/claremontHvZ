from HvZ.models import *
from django.contrib import admin
import HvZ.views

class MissionAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': (('human_title','zombie_title'),('game','day','kind'),('human_image','zombie_image'),'show_players','result')
		}),
		('Story', {
			'classes': ['wide', 'collapse'],
			'fields': (('human_pre_story','zombie_pre_story'),('human_win_story','zombie_lose_story'),('human_draw_story','zombie_draw_story'),('human_lose_story','zombie_win_story'))
		}),
		('Mechanics', {
			'classes': ['wide', 'collapse'],
			'fields': (('human_rules','zombie_rules'),('human_goals','zombie_goals'))
		}),
		('Rewards', {
			'classes': ['wide', 'collapse'],
			'fields': (('human_pre_reward','zombie_pre_reward'),('human_win_reward','zombie_lose_reward'),('human_draw_reward','zombie_draw_reward'),('human_lose_reward','zombie_win_reward'))
		}),
		('SMS', {
			'classes': ['wide', 'collapse'],
			'fields': ('human_SMS','zombie_SMS')
		})
	)

	list_display = ('human_title','zombie_title','day','kind','show_players','result')
	list_display_links = ('human_title','zombie_title')
	list_editable = ('show_players','result')
	list_filter = ('game','day','kind','show_players','result')

	def changelist_view(self, request, extra_context=None):
		if not request.GET.has_key('game__id__exact'):
			q = request.GET.copy()
			q['game__id__exact'] = 2
			request.GET = q
			request.META['QUERY_STRING'] = request.GET.urlencode()
		return super(MissionAdmin,self).changelist_view(request, extra_context=extra_context)

class CharacterInline(admin.TabularInline):
	model = Character

class PlayerAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','school','dorm','grad_year','bad_meals','hash')
	list_display_links = ('first_name','last_name')
	list_filter = ('school','grad_year')
	list_per_page = 100
	ordering = ('user',)
	search_fields = ['user__first_name','user__last_name','user__email','cell']
	inlines = [ CharacterInline, ]

class CharacterAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','school','dorm','team','upgrade','feed','bonus')
	list_display_links = ('first_name','last_name')
	list_editable = ('upgrade','team','feed','bonus')
	list_filter = ('game','team','upgrade')
	search_fields = ['player__user__first_name','player__user__last_name','player__user__email','player__cell','feed']

	def changelist_view(self, request, extra_context=None):
		if not request.GET.has_key('game__id__exact'):
			q = request.GET.copy()
			q['game__id__exact'] = 2
			request.GET = q
			request.META['QUERY_STRING'] = request.GET.urlencode()
		return super(CharacterAdmin,self).changelist_view(request, extra_context=extra_context)

class MealAdmin(admin.ModelAdmin):
	list_display = ('game','eater','eaten','time','location','description')
	list_display_links  = ('eater','eaten')
	list_filter = ('game',)

	def changelist_view(self, request, extra_context=None):
		if not request.GET.has_key('game__id__exact'):
			q = request.GET.copy()
			q['game__id__exact'] = 2
			request.GET = q
			request.META['QUERY_STRING'] = request.GET.urlencode()
		return super(MealAdmin,self).changelist_view(request, extra_context=extra_context)

class BuildingAdmin(admin.ModelAdmin):
	list_display = ('name','campus','building_type','lat','lng')
	list_editable = ('campus','building_type')
	list_filter = ('campus','building_type')
	search_fields = ['name',]

class RuleAdmin(admin.ModelAdmin):
	list_display = ('title','category','priority')
	list_editable = ('priority',)
	list_filter = ('category',)

admin.site.register(School)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Player, PlayerAdmin)
#admin.site.register(Squad)
admin.site.register(PlayerSetting)
admin.site.register(Game)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Meal,MealAdmin)
#admin.site.register(Award)
#admin.site.register(Achievement)
admin.site.register(Mission, MissionAdmin)
#admin.site.register(MissionPoint)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Plot)
admin.site.register(OnDuty)
admin.site.register(ForumThread)
admin.site.register(ForumPost)
