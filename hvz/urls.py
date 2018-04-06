from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from hvz.main import views

urlpatterns = [
    path('', views.landing_page, name='main_landing'),
    path('admin/', admin.site.urls),
    path('eat/', views.EatView.as_view(), name='eat'),
    path('transfer/success/', views.DonateView.as_view(), name="donate_success"),
    path('transfer/', views.DonateView.as_view(), name="donate"),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path('logout/', views.logout, name='logout'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset_form.html',
        ),
        {'post_reset_redirect': 'password_reset/done/'},
        name="password_reset",
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url='/',
        ),
        name='password_reset_confirm',
    ),
    path('players/', views.player_list, name='player_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/success', views.register_success),

    path('emails/', views.json_get_all_emails, name='emails'),

    path('status/', views.PopStatPage.as_view(), name='stats_index'),
    path('status/tags', views.MealLog.as_view(), name='stats_meal_log'),
    path('status/outbreak', views.OutbreakPage.as_view(), name='stats_outbreak'),
    path('status/ancestry', views.AncestryPage.as_view(), name='stats_ancestry'),
    path(
        'status/json/players.json',
        views.json_player_stats,
        name="data_players",
    ),
    path(
        'status/json/ancestry.json',
        views.json_zombie_ancestry,
        name="data_ancestry",
    ),
    path(
        'status/json/taghistogram.json',
        views.json_tag_histogram,
        name="data_tag_histogram",
    ),
    path(
        'status/json/poptimeseries.json',
        views.json_population_time_series,
        name="data_pop_time_series",
    ),
    path('api/', include('hvz.api.urls'))
]
