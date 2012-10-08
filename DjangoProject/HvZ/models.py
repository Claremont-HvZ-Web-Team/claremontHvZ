from django.db import models
from django.contrib.auth.models import User

from constants import *
from hashlib import md5


class School(models.Model):
    """The 7Cs"""
    name = models.CharField(max_length=7)
    def __unicode__(self):
        return self.name


class Building(models.Model):
    """Building are locations on the 7Cs. Most important are dorms and
    landmarks where missions are"""
    KINDS = (
             ("C", "Academic"),
             ("T", "Athletics"),
             ("D", "Dorm"),
             ("I", "Dining Hall"),
             ("L", "Landmark"),
             ("O", "Other")
    )
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(School, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    building_type = models.CharField(max_length=1, choices=KINDS)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.campus)

    def get_kind(self):
        # BUILDING_LEGEND is found in constants.py
        if self.building_type not in BUILDING_LEGEND:
            return ("Error: %s isn't a valid building character!"
                    % self.building_type)

        return BUILDING_LEGEND[self.building_type]


class Player(models.Model):
    """extra information about users"""
    user = models.OneToOneField(User)
    school = models.ForeignKey(School)
    dorm = models.ForeignKey(Building)
    grad_year = models.PositiveIntegerField(blank=True, null=True)
    cell = models.DecimalField(max_digits=10,
                               decimal_places=0,
                               blank=True,
                               null=True)
    human_pic = models.ImageField(upload_to="img/profile/", blank=True, null=True)
    zombie_pic = models.ImageField(upload_to="img/profile/", blank=True, null=True)
    bad_meals = models.PositiveSmallIntegerField(default=0, blank=False)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def first_name(self):
        return self.user.first_name
    first_name.admin_order_field = 'user__first_name'

    def last_name(self):
        return self.user.last_name
    last_name.admin_order_field = 'user__last_name'

    def is_mod(self):
        return self.user.is_staff

    def has_cell(self):
        return self.cell > 1

    def hash(self):
        return md5(self.school.name+self.user.username+str(self.cell)).hexdigest()[::3]


class Squad(models.Model):
    """Lets players organize themselves into groups"""
    name = models.CharField(max_length=30)
    players = models.ManyToManyField(User)
    description = models.TextField(blank=False)
#    icon = models.ImageField(upload_to="icons/squads/", height_field=100, width_field=100)


class PlayerSetting(models.Model):
    """Mostly contains bools of what types of updates players want to receive"""
    player = models.OneToOneField(Player)

    cell_emergency = models.BooleanField()
    cell_send = models.BooleanField()
    cell_mission_announce = models.BooleanField()
    cell_mission_update = models.BooleanField()
    cell_npc_announce = models.BooleanField()
    cell_npc_update = models.BooleanField()

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
        #self.cell_legendary_announce = False
        #self.cell_legendary_update = False
        self.save()


class Game(models.Model):
    """Games are the events that tie everything together"""
    SEMS = (
            ("S", "Spring"),
            ("F", "Fall")
        )
    semester = models.CharField(max_length=1, choices=SEMS)
    year = models.PositiveIntegerField()
    start_date = models.DateField()

    def __unicode__(self):
        if self.semester == "S":
            return "Spring '" + str(self.year)[-2:]
        else:
            return "Fall '" + str(self.year)[-2:]


class Registration(models.Model):
    """Registration is when a player joins a game"""
    TEAMS = (
             ("H", "Humans"),
             ("Z", "Zombies")
    )

    HIDDEN_UPGRADES = (
        ("R", "Rebel Zombie"),
    )

    player = models.ForeignKey(Player)
    hardcore = models.BooleanField(default=False)
    feed = models.CharField(max_length=6)

    game = models.ForeignKey(Game)
    team = models.CharField(max_length=1, choices=TEAMS, default="H")
    upgrade = models.CharField(max_length=30, blank=True, null=True)
    hidden_upgrade = models.CharField(max_length=1, choices=HIDDEN_UPGRADES, blank=True, null=True)
    bonus = models.PositiveSmallIntegerField(default=0, blank=False)

    def __unicode__(self):
        return ("%s: %s %s" %
                (self.game,
                 self.player.first_name(),
                 self.player.last_name()
                 )
                )

    def first_name(self):
        return self.player.first_name()

    def last_name(self):
        return self.player.last_name()

    def is_mod(self):
        return self.player.is_staff()

    def has_cell(self):
        return self.player.has_cell()

    def school(self):
        return self.player.school

    def dorm(self):
        return self.player.dorm

    def get_meals(self, g):
        return Meal.objects.filter(game=g, eater=self.player).count()+self.bonus


class Meal(models.Model):
    """Meals are what happens when one player eats another"""
    eater = models.ForeignKey(Player, related_name="eater")
    eaten = models.ForeignKey(Player, related_name="eaten")
    game = models.ForeignKey(Game)
    time = models.DateTimeField()
    location = models.ForeignKey(Building, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.game)+": "+str(self.eater)+" ate "+str(self.eaten)


class Award(models.Model):
    """The awards that can be given out"""
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
#    icon = models.ImageField(upload_to="icons/awards/", height_field=100, width_field=100)


class Achievement(models.Model):
    """The link between a player and an award they received"""
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    award = models.ForeignKey(Award)
    earned_time = models.DateTimeField(auto_now_add=True)


class Mission(models.Model):
    """Everything about missions"""
    DAYS = (
            ("0", "Monday"),
            ("1", "Tuesday"),
            ("2", "Wednesday"),
            ("3", "Thursday"),
            ("4", "Friday"),
            ("5", "Saturday")
    )
    KINDS = (
             ("D", "Day"),
             ("T", "Night"),
             ("X", "NPC"),
             ("Y", "Legendary")
    )
    STATUS = (
              ("N", "Not Over"),
              ("HF", "Human Full"),
              ("HP", "Human Partial"),
              ("D", "Draw"),
              ("ZP", "Zombie Partial"),
              ("ZF", "Zombie Full")
    )
    VISIBILITY = (
                  ("H", "Humans Only"),
                  ("Z", "Zombies Only"),
                  ("B", "Both Teams"),
                  ("M", "Moderators Only")
    )

    #Basic info
    human_title = models.CharField(max_length=30, blank=True, null=True)
    zombie_title = models.CharField(max_length=30, blank=True, null=True)
    game = models.ForeignKey(Game)
    day = models.CharField(max_length=1, choices=DAYS)
    kind = models.CharField(max_length=1, choices=KINDS)
    show_players = models.CharField(max_length=1, choices=VISIBILITY, default="M")
    result = models.CharField(max_length=2, choices=STATUS, default="N")

    # This is what the teams see if they get condition, so human_win
    # is what humans see if they win and human_pre is the story they
    # see before the mission happens
    human_pre_story = models.TextField(blank=True, null=True)
    human_win_story = models.TextField(blank=True, null=True)
    human_draw_story = models.TextField(blank=True, null=True)
    human_lose_story = models.TextField(blank=True, null=True)
    zombie_pre_story = models.TextField(blank=True, null=True)
    zombie_win_story = models.TextField(blank=True, null=True)
    zombie_draw_story = models.TextField(blank=True, null=True)
    zombie_lose_story = models.TextField(blank=True, null=True)

    # This is what the teams see in the "rules" or "mechanics" section
    # for each mission
    human_rules = models.TextField(blank=True, null=True)
    zombie_rules = models.TextField(blank=True, null=True)

    # This is what the teams see in the "objectives" section for each
    # mission
    human_goals = models.TextField(blank=True, null=True)
    zombie_goals = models.TextField(blank=True, null=True)

    # This is what the teams see in the "rewards" section for each
    # mission depending on whether they win and if it's complete
    human_pre_reward = models.TextField(blank=True, null=True)
    human_win_reward = models.TextField(blank=True, null=True)
    human_draw_reward = models.TextField(blank=True, null=True)
    human_lose_reward = models.TextField(blank=True, null=True)
    zombie_pre_reward = models.TextField(blank=True, null=True)
    zombie_win_reward = models.TextField(blank=True, null=True)
    zombie_draw_reward = models.TextField(blank=True, null=True)
    zombie_lose_reward = models.TextField(blank=True, null=True)

    # This is what response is returned if someone texts "mission",
    # "mission NPC", or "mission Legendary" to us
    human_SMS = models.CharField(max_length=140, blank=True, null=True)
    zombie_SMS = models.CharField(max_length=140, blank=True, null=True)

    human_image = models.ImageField(upload_to="img/mission/",
                                    blank=True,
                                    null=True)
    zombie_image = models.ImageField(upload_to="img/mission/",
                                     blank=True,
                                     null=True)


    def __unicode__(self):
        return "%s: %s/%s" % (self.game,
                              self.human_title,
                              self.zombie_title)

    def get_day(self):
        return DAYS[int(self.day)]

    def get_kind(self):
        if self.kind=="D":
            return "Day"
        elif self.kind=="T":
            return "Night"
        elif self.kind=="X":
            return "NPC"
        elif self.kind=="Y":
            return "Legendary"

    def get_result(self):
        if self.result=="N":
            return "Not Over"
        elif self.result=="HF":
            return "Human Full Victory"
        elif self.result=="HP":
            return "Human Partial Victory"
        elif self.result=="D":
            return "Draw"
        elif self.result=="ZP":
            return "Zombie Partial Victory"
        elif self.result=="ZF":
            return "Zombie Full Victory"

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

    def get_title(self, team):
        if team=="H":
            return self.human_title
        else:
            return self.zombie_title

    def get_story(self, team):
        if self.show_players=="B" or self.show_players==team:
            ret = ""
            # if everyone can see it or if the team we're
            # requesting for can see it
            if team=="H":
                ret+=self.human_pre_story
            else:
                ret+=self.zombie_pre_story

            if self.result=="HF" or self.result=="HP":
                if team=="H":
                    ret+="\n"+self.human_win_story
                else:
                    ret+="\n"+self.zombie_lose_story
            elif self.result=="D":
                if team=="H":
                    ret+="\n"+self.human_draw_story
                else:
                    ret+=self.zombie_draw_story
            elif self.result=="ZF" or self.result=="ZP":
                if team=="H":
                    ret+="\n"+self.human_lose_story
                else:
                    ret+="\n"+self.zombie_win_story
        else:
            ret =  None
        return ret

    def get_reward(self, team):
        if self.show_players=="B" or self.show_players==team:
            # if everyone can see it or if the team we're
            # requesting for can see it
            if self.result=="N":
                if team=="H":
                    return self.human_pre_reward
                else:
                    return self.zombie_pre_reward
            elif self.result=="HF" or self.result=="HP":
                if team=="H":
                    return self.human_win_reward
                else:
                    return self.zombie_lose_reward
            elif self.result=="D":
                if team=="H":
                    return self.human_draw_reward
                else:
                    return self.zombie_draw_reward
            elif self.result=="ZF" or self.result=="ZP":
                if team=="H":
                    return self.human_lose_reward
                else:
                    return self.zombie_win_reward
        else:
            return None


#Linking missions to locations
class MissionPoint(models.Model):
    LOC_TYPE = (
             ("S", "Start"),
             ("D", "Do Something At"),
             ("F", "Find Something At"),
             ("G", "Go to"),
             ("E", "Escort Someone to"),
             ("C", "Complete Mission here")
    )
    VISIBILITY = (
                  ("H", "Humans Only"),
                  ("Z", "Zombies Only"),
                  ("B", "Both Teams"),
                  ("M", "Moderators Only")
    )
    mission = models.ForeignKey(Mission)
    location = models.ForeignKey(Building)
    kind = models.CharField(max_length=1, choices=LOC_TYPE)
    visibility = models.CharField(max_length=1, choices=VISIBILITY)


class Rule(models.Model):
    """Rules stuff"""
    CATS = (
            ("L", "Location"),
            ("C", "Class"),
            ("B", "Basic")
    )
    title = models.CharField(max_length=30)
    description = models.TextField(blank=False)
    category= models.CharField(max_length=1, choices=CATS)
    examples = models.TextField(blank=True, null=True)
    youtube = models.URLField(verify_exists=True, blank=True, null=True)
    image = models.ImageField(upload_to="img/rule/", blank=True, null=True)
    location = models.ForeignKey(Building, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(blank=False, default=0, help_text="Rules with a higher priority appear earlier in the list.")
    def __unicode__(self):
        return str(self.title)


class Plot(models.Model):
    """For story stuff that isn't mission related"""
    TEAMS = (
             ("H", "Humans"),
             ("Z", "Zombies"),
             ("B", "Both"),
             ("N", "Neither")
    )
    title = models.CharField(max_length=30)
    game = models.ForeignKey(Game)
    show_side = models.CharField(max_length=1, choices=TEAMS)
    story = models.TextField(blank=False)
    reveal_time = models.DateTimeField()
    def __unicode__(self):
        return "%s: %s" % (self.game,
                           self.title)


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


class ForumThread(models.Model):
    TEAMS = (
             ("H", "Humans"),
             ("Z", "Zombies"),
             ("B", "Both"),
    )
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField(blank=True, null=True)
    game = models.ForeignKey('Game', blank=False)
    create_time = models.DateTimeField(auto_now=True, blank=False)
    creator = models.ForeignKey('Player', blank=False)
    visibility = models.CharField(max_length=1, blank=False, choices=TEAMS)

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
    parent = models.ForeignKey('ForumThread', blank=False)
    contents = models.TextField(blank=False)
    create_time = models.DateTimeField(auto_now=True, blank=False)
    creator = models.ForeignKey('Player', blank=False)

    def __unicode__(self):
        return ("%s - %s on %s" %
                (str(self.parent),
                 str(self.creator),
                 self.create_time.strftime("%a %I:%M %p")
                 ))


class MealsPerHour(models.Model):
    game = models.ForeignKey('Game', blank=False)
    start = models.DateTimeField(blank=False)
    meals = models.PositiveSmallIntegerField(blank=False)
