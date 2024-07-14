from celery import shared_task
from django.utils import timezone
from .models import Mentorat, Mentorat_Statut

@shared_task
def fermer_mentorat_automatiquement():
    maintenant = timezone.now().date()
    statut_ferme = Mentorat_Statut.objects.get(nom='fermé')
    mentorats = Mentorat.objects.filter(date_fin__lt=maintenant).exclude(statut=statut_ferme)
    for mentorat in mentorats:
        mentorat.statut = statut_ferme
        mentorat.save()
