from django.contrib import admin

from HVZ.missions import models


class PlotAdminInline(admin.StackedInline):
    model = models.Plot
    prepopulated_fields = {'slug': ('title',)}
    max_num = 2
    fields = (
        'title', 'slug', 'team',
        'before_story', 'victory_story', 'defeat_story',
        'visible', 'reveal_time',
    )


class MissionAdmin(admin.ModelAdmin):
    list_filter = ('game',)

    list_display = ('__unicode__', 'victor',)
    lis_display_links = ('__unicode__',)
    list_editable = ('victor',)

    inlines = (PlotAdminInline,)


admin.site.register(models.Mission, MissionAdmin)

