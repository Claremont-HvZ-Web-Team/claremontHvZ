from django import forms
from django.contrib import admin

from HVZ.rules import models


class RuleForm(forms.ModelForm):
    model = models.BaseRule
    exclude = ('position',)


class RuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'position',)
    list_editable = ('position',)

    class Media:
        js = (
            "scripts/jquery.js",
            "scripts/jquery-ui.js",
            "scripts/rule-sort.js",
        )


rule_types = (
    models.CoreRule,
    models.LocationRule,
    models.ClassRule,
    models.SpecialInfectedRule,
)

for r in rule_types:
    admin.site.register(r, RuleAdmin)
