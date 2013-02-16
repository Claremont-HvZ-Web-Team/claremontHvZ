from django.core.exceptions import PermissionDenied

from HVZ.main.models import Player

class PlayerAwareMixin(object):
    """Passes the current player to the view."""

    def set_player(self, request):
        try:
            self.player = Player.user_to_player(request.user)
        except Player.DoesNotExist:
            raise PermissionDenied("You are not registered for this game!")
