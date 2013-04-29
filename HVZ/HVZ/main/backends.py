from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(object):
    """Taken from http://justcramer.com/2008/08/23/logging-in-with-email-addresses-in-django/"""

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
