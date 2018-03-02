from django.core.validators import MaxLengthValidator
from django.db.models.signals import class_prepared
from django.utils.translation import ugettext as _
from longerusernameandemail import MAX_USERNAME_LENGTH, REQUIRE_UNIQUE_EMAIL


def longer_username_and_email_signal(sender, *args, **kwargs):
    if (sender.__name__ == "User" and
        sender.__module__ == "django.contrib.auth.models"):
        patch_user_model_username(sender)
        patch_user_model_email(sender)
class_prepared.connect(longer_username_and_email_signal)


def patch_user_model_username(model):
    field = model._meta.get_field("username")

    field.max_length = MAX_USERNAME_LENGTH()
    field.help_text = _("Required, %s characters or fewer. Only letters, "
                        "numbers, and @, ., +, -, or _ "
                        "characters." % MAX_USERNAME_LENGTH())

    # patch model field validator because validator doesn't change if we change
    # max_length
    for v in field.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = MAX_USERNAME_LENGTH()


def patch_user_model_email(model):
    field = model._meta.get_field("email")

    field.blank = False
    field._unique = REQUIRE_UNIQUE_EMAIL()
    field.max_length = MAX_USERNAME_LENGTH()
    field.help_text = _("Required, %s characters or fewer. Only letters, "
                        "numbers, and @, ., +, -, or _ "
                        "characters." % MAX_USERNAME_LENGTH())

    # patch model field validator because validator doesn't change if we change
    # max_length
    for v in field.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = MAX_USERNAME_LENGTH()


from django.contrib.auth.models import User

# https://github.com/GoodCloud/django-longer-username/issues/1
# django 1.3.X loads User model before class_prepared signal is connected
# so we patch model after it's prepared

# check if User model username is patched
if User._meta.get_field("username").max_length != MAX_USERNAME_LENGTH():
    patch_user_model_username(User)

# check if user model email is patched
if User._meta.get_field("email").max_length != MAX_USERNAME_LENGTH():
    patch_user_model_email(User)
