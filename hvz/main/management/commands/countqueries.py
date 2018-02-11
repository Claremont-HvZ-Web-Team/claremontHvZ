from django.test.client import Client
from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        c = Client()
        path = args[0] if args else '/players/'

        response = c.get(path, follow=True)

        if response.status_code != 200:
            self.stderr.write('Error %s!' % response.status_code)
        else:
            print (len(connection.queries))
        return
