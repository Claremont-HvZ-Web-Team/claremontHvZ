from django.core.exceptions import PermissionDenied

from HVZ.main.models import Player


class PlayerAwareMixin(object):
    """Passes the current player to the view."""

    player = None

    def get_game(self):
        return None

    def set_player(self, request):
        if self.player:
            return
        try:
            self.player = Player.user_to_player(request.user, self.get_game())
        except Player.DoesNotExist:
            raise PermissionDenied("You are not registered for this game!")
