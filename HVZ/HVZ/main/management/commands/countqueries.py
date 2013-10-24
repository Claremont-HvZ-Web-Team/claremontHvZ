from django.test.client import Client
from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        c = Client()
        response = c.get('/players/')
        if response.status_code != 200:
            self.stderr.write('Error!')
        else:
            print (len(connection.queries))
        return
