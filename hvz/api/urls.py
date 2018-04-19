from django.urls import path, include
from django.conf import settings

from hvz.api.views import Mailer, success
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    # Replace this view with your own
    path('mailer', staff_member_required(Mailer.as_view()), name="mailer"),
    path('success', success, name="mail_success")
    ]
