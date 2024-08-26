# Generated by Django 5.0.2 on 2024-08-26 12:45

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0006_alter_activite_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bourse_Opportinute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateField(auto_created=True, auto_now_add=True, null=True)),
                ('created', models.DateField(auto_created=True, auto_now_add=True, null=True)),
                ('libelle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Titre')),
                ('description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Description')),
                ('image_des', models.FileField(blank=True, null=True, upload_to='Fichiers/', verbose_name='Image Descriptive')),
            ],
        ),
    ]