# Generated by Django 5.0.2 on 2024-06-14 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0007_alter_activite_titre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temoignage',
            name='nom_prenom',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nom et Prenom'),
        ),
    ]