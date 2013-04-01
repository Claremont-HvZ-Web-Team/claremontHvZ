from django.core.exceptions import PermissionDenied

class NoActiveGame(PermissionDenied):
    """Raised when no Game is currently ongoing."""
    pass

class NoUnfinishedGames(PermissionDenied):
    """Raised when there are no upcoming or current Games."""
    pass
