from django.core.exceptions import PermissionDenied, ImproperlyConfigured

class NoActiveGame(PermissionDenied):
    """Raised when no Game is currently ongoing."""
    pass

class NoUnfinishedGames(ImproperlyConfigured):
    """Raised when there are no upcoming or current Games."""
