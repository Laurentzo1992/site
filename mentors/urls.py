from django.urls import path, include
from  . import views
from mentors.views import *



urlpatterns = [
    #gestion site
    path('', views.home, name='home'),
]
