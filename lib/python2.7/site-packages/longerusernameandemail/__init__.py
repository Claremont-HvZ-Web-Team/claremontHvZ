from django.conf import settings


def MAX_USERNAME_LENGTH():
    return getattr(settings, "MAX_USERNAME_LENGTH", 255)


def MAX_EMAIL_LENGTH():
    return getattr(settings, "MAX_EMAIL_LENGTH", 255)


def REQUIRE_UNIQUE_EMAIL():
    return getattr(settings, "REQUIRE_UNIQUE_EMAIL", True)
