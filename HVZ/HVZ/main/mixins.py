from django.core.exceptions import PermissionDenied

from HVZ.main.models import Player, Game


class CurrentGameMixin(object):
    """Passes the current game to the view."""

    _game = None

    @property
    def game(self):
        if self._game:
            return self._game
        try:
            self._game = Game.nearest_game()
        except Game.DoesNotExist:
            raise PermissionDenied("You need to create a game!")

        return self._game


class PlayerAwareMixin(object):
    """Passes the current player to the view."""

    _player = None

    @property
    def player(self):
        if self._player:
            return self._player
        try:
            self._player = Player.user_to_player(self.request.user, self.game)
        except Player.DoesNotExist:
            raise PermissionDenied("You are not registered for this game!")

        return self._player
