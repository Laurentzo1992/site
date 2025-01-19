from django.urls import path, include
from  . import views
from mentors.views import *
from mentors.views import ResetPasswordView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('tableau_de_bord/', views.boad, name='boad'),
    path('login/', views.Login, name='login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('editprofile/<int:id>', views.editprofile, name='editprofile'),
    path('createuser/', views.createuser, name='createuser'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='mentors/password_reset_confirm.html'),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='mentors/password_reset_complete.html'),
         name='password_reset_complete'),
    
    path('about/', views.about, name='about'),
    path('bourse-opportunite/', views.bourse_opportunite, name='bourse_opportunite'),
    path('projet/', views.projet, name='projet'),
    path('Mentors/', views.Mentors, name='Mentors'),
    path('orientation/', views.tableau_orientations, name='orientation'),
    path('get_all_even/', views.get_all_even, name='get_all_even'),
    path('get_all_ressource/', views.get_all_ressource, name='get_all_ressource'),
    path('add_even/', views.add_even, name='add_even'),
    path('add_ressource/', views.add_ressource, name='add_ressource'),
    path('get_all_forum/', views.get_all_forum, name='get_all_forum'),
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
    path('joint_us/add', views.adesion, name='adesion'),
    path('demande_ment/add', views.demande_ment, name='demande_ment'),
    path('valider_mentorat/valid/<int:mentorat_id>/', views.valider_mentorat, name='valider_mentorat'),
    path('fermer_mentorat/fermer/<int:mentorat_id>/', views.fermer_mentorat, name='fermer_mentorat'),
    path('complete_profile', views.complete_profile, name='complete_profile'),
    path('mails_personnalisee/', views.mails_personnalisee, name='mails_personnalisee'),
    
    path('mentore_activites/', views.mentore_activites, name='mentore_activites'),
    path('add_mentore_activite/', views.add_activite, name='add_mentore_activite'),
    path('edit_mentore_activite/<id>', views.edit_activite, name='edit_mentore_activite'),
    path('delete_mentore_activite/<id>', views.delete_activite, name='delete_mentore_activite'),
    path('annule_mentore_activite/<id>', views.annule_mentore_activite, name='annule_mentore_activite'),
    path('clos_mentore_activite/<id>', views.clos_mentore_activite, name='clos_mentore_activite'),
    path('valid_mentore_activite/<id>', views.valid_mentore_activite, name='valid_mentore_activite'),
]




