# Generated by Django 5.0.2 on 2025-05-06 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0004_bourse_opportinute_date_limite_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adession',
            name='competence',
            field=models.TextField(blank=True, null=True, verbose_name='Compétence'),
        ),
        migrations.AddField(
            model_name='adession',
            name='nom_complet',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Nom complet'),
        ),
    ]
