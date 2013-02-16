from django.contrib import admin

from HVZ.missions import models

class PlotAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Mission)
admin.site.register(models.Plot, PlotAdmin)
