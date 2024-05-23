from django.urls import path, include
from  . import views
from mentors.views import *


urlpatterns = [
    #gestion site
    path('', views.home, name='home'),
    path('tableau_de bord/', views.boad, name='boad'),
    path('login/', views.Login, name='login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('editprofile/<int:id>', views.editprofile, name='editprofile'),
    path('createuser/', views.createuser, name='createuser'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('about/', views.about, name='about'),
    path('projet/', views.projet, name='projet'),
    path('Mentors/', views.Mentors, name='Mentors'),
    path('abonnement/<int:id>', views.abonnement, name='abonnement'),
    path('desabonnement/', views.desabonnement, name='desabonnement'),
    path('orientation/', views.tableau_orientations, name='orientation'),
    path('get_all_even/', views.get_all_even, name='get_all_even'),
    path('get_all_ressource/', views.get_all_ressource, name='get_all_ressource'),
    path('add_even/', views.add_even, name='add_even'),
    path('add_ressource/', views.add_ressource, name='add_ressource'),
    path('get_all_forum/', views.get_all_forum, name='get_all_forum'),
    path('send_message/', views.send_message, name='send_message'),
    path('send_message_to_users/', views.send_message_to_users, name='send_message_to_users'),
    path('message_thread/', views.message_thread, name='message_thread'),
    path('mentor_messages/', views.mentor_messages, name='mentor_messages'),
    path('add_forum/', views.add_forum, name='add_forum'),
    path('get_all_forum/add_comment/<int:id>/', views.add_comment, name='add_comment'),
    path('get_all_forum/edit_comment/<int:id>/', views.edit_comment, name='edit_comment'),
    path('add_commune/', views.add_commune, name='add_commune'),
    path('add_etablissement/', views.add_etablissement, name='add_etablissement'),
    path('search/', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
    path('newletter/', views.newletter, name='newletter'),
    path('equipe/', views.equipe, name='equipe'),
    path('storie/', views.storie, name='storie'),
    path('joint_us/', views.joint_us, name='joint_us'),
]
