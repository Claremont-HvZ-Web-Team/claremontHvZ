from django.contrib import admin

from HVZ.main.models import Player, Game, MonolithController

class MonolithControllerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','admin', 'forcefield')
    list_editable = ('admin', 'forcefield')

    def has_add_permission(self, request):
        # Singleton!
        return False

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'feed', 'team', 'upgrade')
    list_filter = ('team', 'upgrade', 'game', 'school', 'grad_year', 'can_oz')
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'feed']


admin.site.register(Player, PlayerAdmin)
admin.site.register(Game)
admin.site.register(MonolithController, MonolithControllerAdmin)
