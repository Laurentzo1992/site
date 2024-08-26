from django.contrib import admin
from mentors.models import *
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE


admin.site.register(Regions)
admin.site.register(Provinces)
admin.site.register(Communes)
admin.site.register(Ressources)
admin.site.register(Forum)
admin.site.register(Status)
admin.site.register(Etablissement)
admin.site.register(Badge)
admin.site.register(CategorieFormation)
admin.site.register(Domaine)
admin.site.register(Evenement)
admin.site.register(Type_oriention)
admin.site.register(Filiere_Serie)
admin.site.register(Debouche)
admin.site.register(Typementorat)
admin.site.register(Niveau_formation)
admin.site.register(Slideimage)
admin.site.register(Profiles)

@admin.register(Presentation)
class PresentationAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

@admin.register(Valeur)
class ValeurAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
    
    
admin.site.register(ForumComment)
admin.site.register(Projets)
admin.site.register(Objectif_Accademique)
admin.site.register(Cannaux_Communication)
admin.site.register(Frequence_Echange)
admin.site.register(Cannaux_Connaissance)
admin.site.register(Faq)
admin.site.register(Partenaire)
admin.site.register(Equipe)
admin.site.register(Storie)
admin.site.register(Politique_Securite)
admin.site.register(Temoignage)
admin.site.register(NewletterEmail)
admin.site.register(Mentorat_Statut)



@admin.register(Mot_du_Fondateur)
class Mot_du_FondateurAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }



@admin.register(MailsPersonnalisee)
class MailsPersonnaliseeAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

@admin.register(Activite)
class ActiviteAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }



@admin.register(Bourse_Opportinute)
class BourseOpportuniteAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
