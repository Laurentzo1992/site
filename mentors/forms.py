# users/forms.py
from django import forms
from django.core.validators import RegexValidator
from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import Group
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
        
        
        
class RessourcesForm(forms.ModelForm):
    class Meta:
        model = Ressources
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
        }


class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = '__all__'
        exclude = ('initiateur',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
            'date_even': forms.DateInput(attrs={'type': 'date'})
        }



class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
        }
        
        



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = [
            'telephone', 'niveau', 'commune', 'village', 'domaine',
            'etablissement', 'profile', 'objectif', 'type_mentorat',
            'photo', 'ojectif_academique', 'cannaux', 'frequesce',
            'connaissance', 'attente'
        ]
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''


    
class MentoratForm(forms.ModelForm):
    class Meta:
        model = Mentorat
        fields = ['date_debut', 'date_fin',]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }



class MentoratValidationForm(forms.ModelForm):
    mentor = forms.ModelChoiceField(
        queryset=Profiles.objects.all(),
        required=True,
    )
    date_debut = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))


    class Meta:
        model = Mentorat
        fields = ['date_debut', 'date_fin', 'mentor', 'demandeur']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'demandeur': forms.Select(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super(MentoratValidationForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['demandeur'].queryset = Profiles.objects.filter(pk=self.instance.demandeur.pk)
            self.fields['demandeur'].initial = self.instance.demandeur
        mentor_group = Group.objects.get(name='mentors')
        self.fields['mentor'].queryset = Profiles.objects.filter(user__groups=mentor_group)

    def clean_demandeur(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.demandeur
        else:
            return self.cleaned_data['demandeur']




class MentoratFrmerForm(forms.ModelForm):
    date_debut = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))


    class Meta:
        model = Mentorat
        fields = ['date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }


 
class ActiviteMentoratForm(forms.ModelForm):
    class Meta:
        model = ActiviteMentorat
        fields = ['titre', 'description','image', 'debut', 'fin', 'etat']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
            'debut': forms.DateInput(attrs={'type': 'date'}),
            'fin': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
