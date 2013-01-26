from django.contrib import admin

from HVZ.main.models import Player, Game, MonolithController

class MonolithControllerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','admin', 'forcefield')
    list_editable = ('admin', 'forcefield')

    def has_add_permission(self, request):
        # Singleton!
        return False

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(MonolithController, MonolithControllerAdmin)
