from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from longerusernameandemail.forms import UserCreationForm, UserChangeForm


class LongerUsernameAndEmailUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    add_form = UserCreationForm
    form = UserChangeForm


admin.site.unregister(User)
admin.site.register(User, LongerUsernameAndEmailUserAdmin)
