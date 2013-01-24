class NoActiveGame(Exception):
    """Raised when no Game is currently ongoing."""
    pass

class NoUnfinishedGames(Exception):
    """Raised when there are no upcoming or current Games."""
