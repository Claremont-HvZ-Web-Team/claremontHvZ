from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.conf import settings

from pybb.permissions import DefaultPermissionHandler

from HVZ.main.models import Player


class ForumPermissionHandler(DefaultPermissionHandler):

    """Permission handling based on the names of the forums.

    Assumes that forums are named after teams!

    """

    def filter_forums(self, user, qs):
        """Players should not be able to see the other team's forums."""

        # Always allow mods
        if user.is_staff:
            return qs

        if not user.is_authenticated():
            raise PermissionDenied("You are not logged in!")

        try:
            vb_team = settings.VERBOSE_TEAMS[Player.user_to_player(user).team]
        except Player.DoesNotExist:
            raise PermissionDenied("You are not in this game!")

        # Display the forums for our team or both teams.
        both_or_ours = Q(name=vb_team) | Q(name=settings.VERBOSE_TEAMS['B'])
        return super(ForumPermissionHandler, self).filter_forums(user, qs).filter(both_or_ours)

    def may_view_forum(self, user, forum):
        """Players should not be able to access the other team's forums."""

        # Always allow mods
        if user.is_staff:
            return True

        # Check if the forum allows both teams.
        if forum.name == settings.VERBOSE_TEAMS['B']:
            return super(ForumPermissionHandler, self).may_view_forum(user, forum)

        # Compare the forum's name to the player's team.
        try:
            team = Player.user_to_player(user).team
        except Player.DoesNotExist:
            return False

        vb_team = settings.VERBOSE_TEAMS[team]
        if forum.name != vb_team:
            return False

        return super(ForumPermissionHandler, self).may_view_forum(user, forum)

    def may_view_topic(self, user, topic):
        if not self.may_view_forum(user, topic.forum):
            return False

        return super(ForumPermissionHandler, self).may_view_topic(user, topic)
