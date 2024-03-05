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
]
