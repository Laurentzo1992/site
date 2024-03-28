from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
import mimetypes


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
    libelle = models.CharField(max_length=20, blank=True, null=True)
    statut = models.ForeignKey(Status, blank=True, null=True, on_delete=models.CASCADE)
    commune = models.ForeignKey(Communes, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.libelle




class Ressources(models.Model):
    titre = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
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
    titre = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    fichier = models.FileField(upload_to='forum_img/', null=True, blank=True)
    initiateur = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    IMAGE_MAX_SIZE = (370, 260)
    
    def resize_image(self):
        image = Image.open(self.fichier)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.fichier.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
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
    
    IMAGE_MAX_SIZE = (70, 60)
    
    def resize_image(self):
        image = Image.open(self.badge)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.badge.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
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





class Evenement(models.Model):
    libelle = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lien = models.CharField(max_length=1000, blank=True, null=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    date_even = models.DateField(blank=True, null=True)
    initiateur = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    def __str__(self):
        return self.libelle 
    
    
    IMAGE_MAX_SIZE = (370, 260)
    
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
        
        
        
        
class Type_oriention(models.Model):
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
    telephone = models.CharField(max_length=20, blank=True, null=True)
    niveau = models.ForeignKey(Niveau_formation, blank=True, null=True, on_delete=models.CASCADE)
    commune = models.ForeignKey(Communes, blank=True, null=True, on_delete=models.CASCADE)
    domaine = models.ForeignKey(CategorieFormation, blank=True, null=True, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, blank=True, null=True, on_delete=models.CASCADE)
    profile = models.TextField(blank=True, null=True)
    ojectif = models.CharField(max_length=200, blank=True, null=True)
    type_mentorat = models.ForeignKey(Typementorat, blank=True, null=True, on_delete=models.CASCADE)
    mentor = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='mentored_profiles')
    photo = models.FileField(upload_to='profile/', null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def unsubscribe(self):
        self.mentor = None
        self.save()
    
    IMAGE_MAX_SIZE = (50, 50)
    
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)

# Créer ou mettre à jour automatiquement le profil lorsqu'un utilisateur est enregistré ou mis à jour
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profiles'):
        Profiles.objects.create(user=instance)
    else:
        instance.profiles.save()
        



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