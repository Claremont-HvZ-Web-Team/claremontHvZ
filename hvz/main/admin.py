from django.contrib import admin

from hvz.main import models

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'feed', 'team', 'role', 'brains', 'can_oz')
    list_filter = (
        'team',
        'game',
        'school',
        'brains',
        'can_oz',
    )
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'feed',
    ]

admin.site.register(models.Game)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Meal)
admin.site.register(models.School)
admin.site.register(models.Building)
admin.site.register(models.Role)
