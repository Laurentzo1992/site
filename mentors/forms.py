# users/forms.py
from django import forms
from django.core.validators import RegexValidator
from django import forms
from .models import *

from .models import ForumComment

#from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom tilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
    
    
    
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
        }




class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageMent
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
        }
