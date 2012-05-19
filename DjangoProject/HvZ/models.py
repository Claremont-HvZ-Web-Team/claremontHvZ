from django.db import models
from django.contrib.auth.models import User

from constants import *

##################
# Building Stuff #
##################
class School(models.Model):
    """The 7Cs"""
    name = models.CharField(max_length=7)
    def __unicode__(self):
        return self.name

class Building(models.Model):
    """Building are locations on the 7Cs. Most important are dorms and
    landmarks where missions are"""
    
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(School,blank=True,null=True)
    lat = models.DecimalField(max_digits=9,decimal_places=6)
    lng = models.DecimalField(max_digits=9,decimal_places=6)
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.campus)

class BuildingKinds(models.Model):
    """BuildingKinds are the way to account for buildings having multiple types"""
    building = models.ForeignKey(Building)
    building_kind = models.CharField(max_length=1,choices=BUILDING_LEGEND_TT)

    def get_kind(self):
        if self.building_type not in BUILDING_LEGEND:
            return ("Error: %s isn't a valid building character!"
                    % self.building_type)

        return BUILDING_LEGEND[self.building_type]


class Dorm(Building):
    #We need a subclass for dorms, I just don't know what it should contain yet.
    residents = models.PositiveSmallIntegerField(blank=False,default=0)

class Classroom(Building):
    #We need a subclass for academic buildings, I just don't know what it should contain yet.
    field = models.CharField(max_length=100)

###############
# Game Things #
###############
class Game(models.Model):
    """Games are the events that tie everything together"""
    SEMS = (
            ("S","Spring"),
            ("F","Fall")
        )
    semester = models.CharField(max_length=1,choices=SEMS)
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    def __unicode__(self):
        if self.semester=="S":
            return "Spring '"+str(self.year)[-2:]
        else:
            return "Fall '"+str(self.year)[-2:]

class Rule(models.Model):
    """Rules stuff"""
    CATS = (
            ("L","Location"),
            ("C","Class"),
            ("B","Basic")
    )
    title = models.CharField(max_length=30)
    description = models.TextField(blank=False)
    category= models.CharField(max_length=1,choices=CATS)
    examples = models.TextField(blank=True,null=True)
    youtube = models.URLField(verify_exists=True,blank=True,null=True)
    image = models.ImageField(upload_to="img/rule/",blank=True,null=True)
    location = models.ForeignKey(Building,blank=True,null=True)
    priority = models.PositiveSmallIntegerField(blank=False,default=0,help_text="Rules with a higher priority appear earlier in the list.")
    def __unicode__(self):
        return str(self.title)

class Award(models.Model):
    """The awards that can be given out"""
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="icons/awards/")

#################
# Mission Stuff #
#################
class Mission(models.Model):
    """Everything about missions"""

    #Basic info
    human_title = models.CharField(max_length=30,blank=True,null=True)
    zombie_title = models.CharField(max_length=30,blank=True,null=True)
    game = models.ForeignKey(Game)
    day = models.CharField(max_length=1,choices=DAYS_TT)
    kind = models.CharField(max_length=1,choices=MISSION_LEGEND_TT)
    show_players = models.CharField(max_length=1,choices=VISIBILITY_TT,default="M")
    result = models.CharField(max_length=2,choices=VICTORY_TT,default="N")

    # This is story stuff. Both sides see the quote
    # story is what they see before and during the mission
    # outcome is what they see after the mission
    quote = models.TextField(blank=True,null=True)
    human_story = models.TextField()
    human_outcome = models.TextField()
    zombie_story = models.TextField()
    zombie_outcome = models.TextField()

    # This is what the teams see in the "rules" or "mechanics" section
    # for each mission, it also includes goals
    human_rules = models.TextField(blank=True,null=True)
    zombie_rules = models.TextField(blank=True,null=True)

    # This is what the teams see in the "rewards" section for each
    # mission
    human_reward = models.TextField(blank=True,null=True)
    zombie_reward = models.TextField(blank=True,null=True)

    # This is what response is returned if someone texts "mission",
    # "mission NPC", or "mission Legendary" to us
    human_SMS = models.CharField(max_length=140,blank=True,null=True)
    zombie_SMS = models.CharField(max_length=140,blank=True,null=True)

    def __unicode__(self):
        return "%s: %s/%s" % (self.game,
                              self.human_title,
                              self.zombie_title)

    def get_day(self):
        return DAYS[int(self.day)]

    def get_kind(self):
        return MISSION_LEGEND[self.kind]

    def get_result(self):
        return VICTORY[self.result]

    def get_result_order(self):
        if self.result=="N":
            return "1"
        elif self.result=="HF":
            return "2"
        elif self.result=="HP":
            return "3"
        elif self.result=="D":
            return "4"
        elif self.result=="ZP":
            return "5"
        elif self.result=="ZF":
            return "6"

    def get_title(self,team):
	if team=="H":
		return self.human_title
	else:
		return self.zombie_title

    def get_story(self,team):
	if self.show_players=="B" or self.show_players==team:
		ret = ""
		if team=="H":
			ret+=self.human_story
		else:
			ret+=self.zombie_story

		if self.result!="N":
			if team=="H":
				ret+="<br/>"+self.human_outcome
			else:
				ret+="<br/>"+self.zombie_outcome
	else:
		ret =  "No Story is visible for this mission yet."
	return ret

    def get_reward(self,team):
	if self.show_players=="B" or self.show_players==team:
		if team=="H":
			return self.human_reward
		else:
			return self.zombie_reward
	else:
		return "No Reward is visible for this mission yet."

#Link mission to Image
class MissionPic(models.Model):
    mission = models.ForeignKey(Mission)
    image = models.ImageField(upload_to="img/mission/")
    visibility = models.CharField(max_length=1,choices=VISIBILITY_TT)

#Link mission to location
class MissionPoint(models.Model):
    mission = models.ForeignKey(Mission)
    location = models.ForeignKey(Building)
    kind = models.CharField(max_length=1,choices=LOCATION_LEGEND_TT)
    visibility = models.CharField(max_length=1,choices=VISIBILITY_TT)

    def get_kind(self):
        return LOCATION_LEGEND[self.kind]

class Plot(models.Model):
    """For story stuff that isn't mission related"""
    title = models.CharField(max_length=30)
    game = models.ForeignKey(Game)
    show_side = models.CharField(max_length=1,choices=VISIBILITY_TT)
    story = models.TextField(blank=False)
    reveal_time = models.DateTimeField()
    def __unicode__(self):
	return "%s: %s" % (self.game,self.title)
    
################
# Player Stuff #
################
class Player(models.Model):
    """extra information about users"""
    user = models.OneToOneField(User)
    school = models.ForeignKey(School)
    dorm = models.ForeignKey(Dorm)
    grad_year = models.PositiveIntegerField(blank=True,null=True)
    cell = models.DecimalField(max_digits=10,decimal_places=0,blank=True,null=True)
    bad_meals = models.PositiveSmallIntegerField(default=0,blank=False)
    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def first_name(self):
        return self.user.first_name
    first_name.admin_order_field='user__first_name'

    def last_name(self):
        return self.user.last_name
    last_name.admin_order_field='user__last_name'

    def is_mod(self):
        return self.user.is_staff

    def has_cell(self):
        return self.cell > 1

class PlayerSetting(models.Model):
    """Player settings"""
    player = models.OneToOneField(Player)
    
    #cell related settings
    cell_emergency = models.BooleanField(default=True)
    cell_send = models.BooleanField(default=False)
    cell_mission_announce = models.BooleanField(default=False)
    cell_mission_update = models.BooleanField(default=False)
    cell_npc_announce = models.BooleanField(default=False)
    cell_npc_update = models.BooleanField(default=False)
    cell_legendary_announce = models.BooleanField(default=False)
    cell_legendary_update = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s's Settings" % self.player

    #Command to unsubscribe from all texting services
    def quit_cell(self):
        self.cell_emergency = False
        self.cell_send = False
        self.cell_mission_announce = False
        self.cell_mission_update = False
        self.cell_npc_announce = False
        self.cell_npc_update = False
        self.cell_legendary_announce = False
        self.cell_legendary_update = False
        self.save()

class PlayerProfile(models.Model):
    player = models.OneToOneField(Player)
    human_pic = models.ImageField(upload_to="img/profile/",blank=True,null=True)
    zombie_pic = models.ImageField(upload_to="img/profile/",blank=True,null=True)
    bio = models.TextField()

    #visibility related settings
    show_school = models.CharField(max_length=1,choices=VISIBILITY_TT,default="B")
    show_dorm = models.CharField(max_length=1,choices=VISIBILITY_TT,default="B")
    show_year = models.CharField(max_length=1,choices=VISIBILITY_TT,default="B")
    show_cell = models.CharField(max_length=1,choices=VISIBILITY_TT,default="B")

###################
# Character Stuff #
###################
class Character(models.Model):
    """Characters are the instances of players in games"""
    TEAMS = (
             ("H","Humans"),
             ("Z","Zombies")
    )
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    team = models.CharField(max_length=1,choices=TEAMS,default="H")
    upgrade = models.CharField(max_length=30,blank=True,null=True)
    hardcore = models.BooleanField(default=False)
    #Meals is now total meals to avoid a costly DB lookup when you want to know how many meals someone has
    meals = models.PositiveSmallIntegerField(default=0,blank=False)
    #These 3 fields are redundant most of the time, but are useful for archiving games
    lives_in = models.ForeignKey(Dorm)
    goes_to = models.ForeignKey(School)
    year = models.CharField(max_length=1,choices=CLASS_YEAR_TT,blank=True,null=True)
    
    def __unicode__(self):
        return ("%s: %s %s" %
                (self.game,
                 self.player.first_name(),
                 self.player.last_name()
                 )
                )

    def get_year(self):
        return CLASS_YEAR[self.year]

class FeedCode(models.Model):
    """We have to pull this out now that feed cards have extra options"""
    #If blank, then the meal is just a reward not linked to a player
    character = models.ForeignKey(Character,blank=True)
    #code is the 6 letter feed code
    code = models.CharField(max_length=6)
    #value is how many meals the eater's mealcount should be incremented by when they eat this card
    value = models.PositiveSmallIntegerField(default=1)
    #turns is true if eating this code turns the player, if false they stay human after having this card eaten
    #the meals page and timeline page should note this as "almost ate", "barely escaped", or the like
    turns = models.BooleanField(default=True)

class Meal(models.Model):
    """Meals are what happens when one player eats another"""
    eater = models.ForeignKey(Player,related_name="eater")
    eaten = models.ForeignKey(Player,related_name="eaten")
    game = models.ForeignKey(Game)
    time = models.DateTimeField()
    escaped = models.BooleanField(default=False)
    location = models.ForeignKey(Building,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return str(self.game)+": "+str(self.eater)+" ate "+str(self.eaten)

class Classes(models.Model):
    #A way that players can give a rough outline of where they will be when so they can better coordinate being in groups for safety. 
    character = models.ForeignKey(Character)
    classroom = models.ForeignKey(Classroom)
    day = models.CharField(max_length=1,choices=DAYS_TT)
    arrive = models.CharField(max_length=1,choices=TIMES_TT)
    leave = models.CharField(max_length=1,choices=TIMES_TT)

    def get_day(self):
        return DAYS[int(self.day)]

    def get_arrive(self):
        return TIMES[self.arrive]

    def get_leave(self):
        return TIMES[self.leave]

    def __unicode__(self):
        return str(self.character)+" is in "+str(self.classroom)+" on "+self.get_day()+" from "+self.get_arrive()+" until "+self.get_leave()

class Achievement(models.Model):
    """The link between a character and an award they received"""
    character = models.ForeignKey(Character)
    game = models.ForeignKey(Game)
    award = models.ForeignKey(Award)
    earned_time = models.DateTimeField()

###############
# Squad Stuff #
###############
class Squad(models.Model):
    """Lets players organize themselves into groups"""
    name = models.CharField(max_length=30);
    game = models.ForeignKey(Game)
    description = models.TextField(blank=False)
    icon = models.ImageField(upload_to="icons/squads/")

class SquadMember(models.Model):
    character = models.ForeignKey(Character)
    squad = models.ForeignKey(Squad)
    role = models.CharField(max_length=50)
    approve_new = models.BooleanField(default=False)
    
###############
# Forum Stuff #
###############
class ForumThread(models.Model):
    TEAMS = (
             ("H","Humans"),
             ("Z","Zombies"),
             ("B","Both"),
    )
    title = models.CharField(max_length=30,blank=False)
    description = models.TextField(blank=True,null=True)
    game = models.ForeignKey('Game',blank=False)
    create_time = models.DateTimeField(auto_now=True,blank=False)
    creator = models.ForeignKey('Player',blank=False)
    visibility = models.CharField(max_length=1,blank=False,choices=TEAMS)

    def __unicode__(self):
	return "%s (%s: %s)" % (self.title,
                                self.game,
                                self.visibility)

    def post_count(self):
	return ForumPost.objects.filter(parent=self).count()

    def last_post(self):
	posts = ForumPost.objects.filter(parent=self).order_by('-create_time')
	if posts.exists():
		return posts[0]
	else:
		return None

class ForumPost(models.Model):
    parent = models.ForeignKey('ForumThread',blank=False)
    contents = models.TextField(blank=False)
    create_time = models.DateTimeField(auto_now=True,blank=False)
    creator = models.ForeignKey('Player',blank=False)

    def __unicode__(self):
	return ("%s - %s on %s" %
                (str(self.parent),
                 str(self.creator),
                 self.create_time.strftime("%a %I:%M %p")
                 ))

########
# Misc #
########
class OnDuty(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mod = models.ForeignKey(Player,
                            limit_choices_to = {
            'cell__gte':'1',
            'user__is_staff':'True'
            }
                            )
    def __unicode__(self):
        return (
            "%s: %s until %s" % (self.mod.user.first_name,
                                 self.start_time.strftime("%a %I:%M %p"),
                                 self.end_time.strftime("%a %I:%M %p")
                                 ))


class MealsPerHour(models.Model):
	game = models.ForeignKey(Game,blank=False)
	start = models.DateTimeField(blank=False)
	meals = models.PositiveSmallIntegerField(blank=False)
