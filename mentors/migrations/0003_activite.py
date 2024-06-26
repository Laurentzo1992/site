# Generated by Django 5.0.2 on 2024-06-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0002_presentation_about1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateField(auto_created=True, auto_now_add=True, null=True)),
                ('created', models.DateField(auto_created=True, auto_now_add=True, null=True)),
                ('titre', models.CharField(blank=True, max_length=50, null=True, verbose_name='Titre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('image_des', models.FileField(blank=True, null=True, upload_to='Fichiers/', verbose_name='Image Descriptive')),
            ],
        ),
    ]
