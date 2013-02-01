from django.contrib import admin

from HVZ.rules import models

admin.site.register(models.CoreRule)
admin.site.register(models.LocationRule)
admin.site.register(models.ClassRule)
admin.site.register(models.SpecialInfectedRule)
