from django.test.client import Client
from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        c = Client()
        path = args[0] or '/players/'

        response = c.get(path)

        if response.status_code != 200:
            self.stderr.write('Error %s!' % response.status_code)
        else:
            print (len(connection.queries))
        return
