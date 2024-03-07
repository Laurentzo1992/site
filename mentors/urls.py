from django.urls import path, include
from  . import views
from mentors.views import *


urlpatterns = [
    #gestion site
    path('', views.home, name='home'),
    path('login', views.Login, name='login'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('editprofile/<int:id>', views.editprofile, name='editprofile'),
    path('createuser', views.createuser, name='createuser'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('about', views.about, name='about'),
    path('Mentors', views.Mentors, name='Mentors'),
    path('abonnement/<int:id>', views.abonnement, name='abonnement'),
    path('desabonnement/', views.desabonnement, name='desabonnement'),
    path('orientation', views.tableau_orientations, name='orientation'),
    path('get_all_even', views.get_all_even, name='get_all_even'),
    path('get_all_ressource', views.get_all_ressource, name='get_all_ressource'),
    path('add_even', views.add_even, name='add_even'),
    path('add_ressource', views.add_ressource, name='add_ressource'),
    path('get_all_forum', views.get_all_forum, name='get_all_forum'),
    path('add_forum', views.add_forum, name='add_forum'),
]
