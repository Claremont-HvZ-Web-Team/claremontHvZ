from django.db.models import Q
from django.conf import settings

from pybb.permissions import DefaultPermissionHandler

from HVZ.main.models import Player

class ForumPermissionHandler(DefaultPermissionHandler):

    """Permission handling based on the names of the forums.

    Assumes that forums are named after teams!

    """

    def filter_forums(self, user, qs):

        return qs.filter(name="OOGA")
        """Players should not be able to see the other team's forums."""

        vb_team = settings.VERBOSE_TEAMS[Player.user_to_player(user).team]

        # Display the forums for our team or both teams.
        both_or_ours = Q(name=vb_team) | Q(name=settings.VERBOSE_TEAMS['B'])
        return super(ForumPermissionHandler, self).filter_forums(user, qs).filter(both_or_ours)

    def may_view_forum(self, user, forum):
        """Players should not be able to access the other team's forums."""

        # Check if the forum allows both teams.
        if forum.name != VERBOSE_TEAMS['B']:
            return super(ForumPermissionHandler, self).may_view_forum(user, forum)

        # Compare the forum's name to the player's team.
        vb_team = settings.VERBOSE_TEAMS[Player.user_to_player(user).team]
        if forum.name != vb_team:
            return False

        return super(ForumPermissionHandler, self).may_view_forum(user, forum)
