from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
import mimetypes
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.core.mail import send_mail
from django.conf import settings
from tinymce.models import HTMLField
from tinymce import models as tinymce_models

class Regions(models.Model):
    numero = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Numero d'ordre")
    nomreg = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nom de la region")
    cheflieu = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Chef lieu")
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    class Meta:
        verbose_name = "Regions"
        verbose_name_plural = "Region"
        
    def __str__(self):
        return self.nomreg




class Provinces(models.Model):
    numero = models.CharField(max_length=1000, blank=True, null=True,verbose_name="Numero d'ordre")
    nomprov = models.CharField(max_length=500, blank=True, null=True, verbose_name="Nom de la province")
    region = models.ForeignKey(Regions, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Region")
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Provinces"
        verbose_name_plural = "Province"
        
    def __str__(self):
        return self.nomprov
    



class Communes(models.Model):
    nom_commune = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nom de la commune")
    province = models.ForeignKey(Provinces, blank=True, null=True, on_delete=models.CASCADE,verbose_name="Province")
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.nom_commune
    
class Status(models.Model):
    statut = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.statut

class Etablissement(models.Model):
    libelle = models.CharField(max_length=200, blank=True, null=True)
    statut = models.ForeignKey(Status, blank=True, null=True, on_delete=models.CASCADE)
    commune = models.ForeignKey(Communes, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.libelle




class Ressources(models.Model):
    titre = models.CharField(max_length=50, null=True, blank=True, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    ressource = models.FileField(upload_to='Fichiers/', null=True, blank=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    def __str__(self):
        return self.titre
    
    
    def get_mime_type(self):
        if self.ressource:
            return mimetypes.guess_type(self.ressource.path)[0]
        else:
            return None
        
        
class Forum(models.Model):
    titre = models.CharField(max_length=50, null=True, blank=True, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    fichier = models.FileField(upload_to='forum_img/', null=True, blank=True, verbose_name="Image illustrative")
    initiateur = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    IMAGE_MAX_SIZE = (370, 260)
    
    def resize_image(self):
        if self.fichier:
            image = Image.open(self.fichier)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            # sauvegarde de l’image redimensionnée dans le système de fichiers
            # ce n’est pas la méthode save() du modèle !
            image.save(self.fichier.path)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.fichier:
            self.resize_image()
        
        
    def __str__(self):
        return self.titre
        
        
class ForumComment(models.Model):
    comment = models.TextField(blank=True, null=True, verbose_name="Commentaire")
    forum = models.ForeignKey(Forum, blank=True, null=True, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    

    def __str__(self):
        return self.comment 
    
    
class Badge(models.Model):
    classe_badge = models.CharField(max_length=100, blank=True, null=True)
    badge = models.FileField(upload_to='images/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    IMAGE_MAX_SIZE = (39, 60)
    
    def resize_image(self):
        if self.badge:
            image = Image.open(self.badge)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.badge.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.badge:
            self.resize_image()
        
    
    
    def __str__(self):
        return self.classe_badge
    
    
class CategorieFormation(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
class Domaine(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    categorie = models.ForeignKey(CategorieFormation, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    def __str__(self):
        return self.libelle



        
class Type_oriention(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
    
class Objectif_Accademique(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
    
class Cannaux_Communication(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle



class Frequence_Echange(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
    

class Cannaux_Connaissance(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle



class Filiere_Serie(models.Model):
    type = models.ForeignKey(Type_oriention, blank=True, null=True, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
    
class Debouche(models.Model):
    debouche = models.ForeignKey(Filiere_Serie, blank=True, null=True, on_delete=models.CASCADE)
    libelle = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
    
class Typementorat(models.Model):
    libelle = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
class Niveau_formation(models.Model):
    libelle = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.libelle
  
    
    
class Profiles(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Téléphone')
    niveau = models.ForeignKey(Niveau_formation, blank=True, null=True, on_delete=models.CASCADE)
    can_be_mentor = models.BooleanField(default=False, verbose_name="Peut etre mentor?")
    commune = models.ForeignKey(Communes, blank=True, null=True, on_delete=models.CASCADE)
    village = models.CharField(max_length=20, blank=True, null=True)
    domaine = models.ForeignKey(CategorieFormation, blank=True, null=True, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, blank=True, null=True, on_delete=models.CASCADE)
    profile = models.TextField(blank=True, null=True)
    objectif = models.CharField(max_length=200, blank=True, null=True)
    type_mentorat = models.ForeignKey(Typementorat, blank=True, null=True, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='profile/', null=True, blank=True)
    ojectif_academique = models.ForeignKey(Objectif_Accademique, blank=True, null=True, on_delete=models.CASCADE)
    cannaux = models.ForeignKey(Cannaux_Communication, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Quel canal de communication préférez vous pour echanger avec le mentor')
    frequesce = models.ForeignKey(Frequence_Echange, blank=True, null=True, on_delete=models.CASCADE, verbose_name='A quelle fréquence vous vous echangez avec le mentor?')
    connaissance = models.ForeignKey(Cannaux_Connaissance, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Comment avez vous connu MEntorMe')
    attente = models.TextField(blank=True, null=True)
    total_time_on_platform = models.DurationField(default=timezone.timedelta())
    last_login = models.DateTimeField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    
    IMAGE_MAX_SIZE = (50, 50)
    
    
    
    def __str__(self):
        return self.user.username
    
    def unsubscribe(self):
        self.mentor = None
        self.save()

    
    def resize_image(self):
        if self.photo:
            image = Image.open(self.photo)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            # sauvegarde de l’image redimensionnée dans le système de fichiers
            # ce n’est pas la méthode save() du modèle !
            image.save(self.photo.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            self.resize_image()
        
    def total_time_on_platform_hours(self):
        total_hours = self.total_time_on_platform.total_seconds() / 3600
        return total_hours
    
    
    def formatted_total_time_on_platform(self):
        total_seconds = int(self.total_time_on_platform.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}min {seconds}sec"

class Mentor(models.Model):
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, limit_choices_to={'can_be_mentor': True})
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    def __str__(self):
        return self.profile.user.first_name+ " "+self.profile.user.last_name

class Mentore(models.Model):
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, limit_choices_to={'can_be_mentor': False})
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    def __str__(self):
        return self.profile.user.first_name+ " "+self.profile.user.last_name


# Mettre à jour le temps total passé sur la plateforme à chaque fois qu'un utilisateur se déconnecte
@receiver(user_logged_out)
def update_total_time_on_platform(sender, user, **kwargs):
    profile = user.profiles
    if profile.last_login:
        time_difference = timezone.now() - profile.last_login
        profile.total_time_on_platform += time_difference
        profile.last_login = None
        profile.save()



# Mettre à jour le dernier temps de connexion à chaque fois qu'un utilisateur se connecte
@receiver(user_logged_in)
def update_last_login(sender, user, **kwargs):
    user.profiles.last_login = timezone.now()
    user.profiles.save()



# Créer ou mettre à jour automatiquement le profil lorsqu'un utilisateur est enregistré ou mis à jour
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profiles'):
        Profiles.objects.create(user=instance)
    else:
        instance.profiles.save()

class Mentorat_Statut(models.Model):
    statut = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    def __str__(self):
        return self.statut
    

class Mentorat(models.Model):
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    demandeur = models.ForeignKey(Profiles, related_name='demandes_mentorat', on_delete=models.CASCADE, blank=True, null=True)
    mentor = models.ForeignKey(Profiles, related_name='mentorats', on_delete=models.CASCADE, blank=True, null=True)
    statut = models.ForeignKey(Mentorat_Statut, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    
    def __str__(self):
        return f'Mentorat from {self.demandeur} with {self.mentor} (Status: {self.statut})'

   

class Mentorat_Score(models.Model):
    mentore_note = models.CharField(max_length=10, blank=True, null=True)
    mentorat_score = models.ForeignKey(Mentorat, on_delete=models.CASCADE, blank=True, null=True)
    
    
class Slideimage(models.Model):
    image = models.FileField(upload_to='images/', null=True, blank=True)
    titre1 = models.CharField(max_length=200, blank=True, null=True)
    titre2 = models.CharField(max_length=200, blank=True, null=True)
    titre3 = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    
    def __str__(self):
        return self.titre1
    
class Presentation(models.Model):
    about1 = models.TextField(blank=True, null=True, verbose_name="A propos de 2click")
    about = models.TextField(blank=True, null=True, verbose_name="Qui nous sommes")
    mission = models.TextField(blank=True, null=True, verbose_name="Notre mission")
    vision = models.TextField(blank=True, null=True, verbose_name="Notre vision")
    presentation_video = models.FileField(upload_to='video/', null=True, blank=True)
    nom_site = models.CharField(max_length=200, blank=True, null=True, default="OSER")
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    
    def __str__(self):
        return self.nom_site
    
    
    
class Projets(models.Model):
    titre = models.CharField(max_length=200, blank=True, null=True)
    contenu = models.TextField(blank=True, null=True)
    Visuel = models.FileField(upload_to='images/', null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    
    def __str__(self):
        return self.titre
    
    
    
class Valeur(models.Model):
    titre = models.CharField(max_length=200, blank=True, null=True)
    valeur = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    
    def __str__(self):
        return self.valeur
    
    
class MessageMent(models.Model):
    sender = models.ForeignKey(User, blank=True, null=True, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, blank=True, null=True, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, verbose_name="Contenu")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    
class Inbox(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    messages = models.ManyToManyField(MessageMent)
    created = models.DateField(auto_now_add=True, blank=True, null=True)
    modified = models.DateField(auto_now=True, blank=True, null=True)
    
    
    
    
class Faq(models.Model):
    la_question = models.CharField(max_length=200, blank=True, null=True)
    la_reponse = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)
    modified = models.DateField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.la_question
    

class Partenaire(models.Model):
    nom = models.CharField(max_length=200, blank=True, null=True)
    contenue = models.TextField(blank=True, null=True)
    patenaire_image = models.FileField(upload_to='images/', null=True, blank=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)
    modified = models.DateField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.patenaire_image.url
    
    
    
class NewletterEmail(models.Model):
    useremail = models.EmailField(blank=True, null=True, unique=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)
    modified = models.DateField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.useremail
    
    


class Equipe(models.Model):
    nom_prenom = models.CharField(max_length=200, verbose_name="Nom et Prenom", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    photo = models.FileField(upload_to='images/', verbose_name="Photo", blank=True, null=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)
    modified = models.DateField(auto_now=True, blank=True, null=True)

    IMAGE_MAX_SIZE = (170, 170)

    def __str__(self):
        return self.nom_prenom
            
            
            

class Storie(models.Model):
    nom_prenom = models.CharField(max_length=200, verbose_name="Nom et Prenom", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    photo = models.FileField(upload_to='images/', verbose_name="Photo", blank=True, null=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)
    modified = models.DateField(auto_now=True, blank=True, null=True)

    IMAGE_MAX_SIZE = (170, 170)

    def __str__(self):
        return self.nom_prenom

    def resize_image(self):
        if self.photo:
            image = Image.open(self.photo)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            # Sauvegarde de l’image redimensionnée dans le système de fichiers
            image.save(self.photo.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            self.resize_image()
            
            
            
class Evenement(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True, verbose_name="Libelle")
    description = models.TextField(blank=True, null=True,  verbose_name="Description")
    lien = models.CharField(max_length=1000, blank=True, null=True,  verbose_name="Lien de l'évènement")
    image = models.FileField(upload_to='images/', null=True, blank=True,  verbose_name="Image illustrative")
    date_even = models.DateField(blank=True, null=True,  verbose_name="Date de l'évènement")
    initiateur = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    IMAGE_MAX_SIZE = (370, 260)
    
    def __str__(self):
        return self.libelle 
    

    
    def resize_image(self):
        if self.image:
            image = Image.open(self.image)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()
        
        
@receiver(post_save, sender=Evenement)
def send_newsletter_emails(sender, instance, **kwargs):
    if kwargs['created']:
        if  NewletterEmail.objects.all().exists():
            for subscriber in  NewletterEmail.objects.all():
                send_mail(
                    'Nouvel événement disponible',
                    f'Un nouvel événement "{instance.libelle} {instance.description}" est disponible.le lien {instance.lien}',
                    settings.EMAIL_HOST,
                    [subscriber.useremail],
                    fail_silently=True,
                )
                
                
                
                


class Politique_Securite(models.Model):
    titre = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_even = models.DateField(blank=True, null=True,  verbose_name="Date de l'activité")
    created = models.DateField(auto_now_add=True, blank=True, null=True)
    modified = models.DateField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.titre
    
    
    
    
class Temoignage(models.Model):
    nom_prenom = models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom et Prenom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    photo = models.FileField(upload_to='Fichiers/', null=True, blank=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    def __str__(self):
        return self.nom_prenom
    
    
    
class Activite(models.Model):
    titre = models.CharField(max_length=200, blank=True, null=True,verbose_name="Titre")
    #description = models.HTMLField(blank=True, null=True, verbose_name="Description")
    description = tinymce_models.HTMLField(blank=True, null=True, verbose_name="Description")
    image_des = models.FileField(upload_to='Fichiers/', null=True, blank=True, verbose_name="Image Descriptive")
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    def __str__(self):
        return self.titre
    
    
class Adession(models.Model):
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    tel = models.CharField(max_length=15, blank=True, null=True, verbose_name="Téléphone")
    motivation = models.TextField(null=True, blank=True, verbose_name="Motivation")
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    def __str__(self):
        return self.email
    
    


class Mot_du_Fondateur(models.Model):
    STATUS = (
    ('actif', ('mot actif')),
    ('inactif', ('mot inactif')),
    )
    
    mot = models.TextField(blank=True, null=True, verbose_name="Mot du fondateur")
    statut = models.CharField(max_length=32, choices=STATUS, blank=True, null=True, verbose_name="Statut")
    
    
    def __str__(self):
        return self.mot
    
class MailsPersonnalisee(models.Model):
    intituler = models.CharField( max_length=150)
    objet = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField()
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now=True)
    
    

    def __str__(self):
        return self.intituler

