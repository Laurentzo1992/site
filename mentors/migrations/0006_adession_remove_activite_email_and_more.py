# Generated by Django 5.0.2 on 2024-06-12 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0005_remove_activite_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateField(auto_created=True, auto_now_add=True, null=True)),
                ('created', models.DateField(auto_created=True, auto_now_add=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('tel', models.CharField(blank=True, max_length=15, null=True, verbose_name='Téléphone')),
                ('motivation', models.TextField(blank=True, null=True, verbose_name='Motivation')),
            ],
        ),
        migrations.RemoveField(
            model_name='activite',
            name='email',
        ),
        migrations.RemoveField(
            model_name='activite',
            name='motivation',
        ),
        migrations.RemoveField(
            model_name='activite',
            name='tel',
        ),
        migrations.AddField(
            model_name='activite',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='activite',
            name='image_des',
            field=models.FileField(blank=True, null=True, upload_to='Fichiers/', verbose_name='Image Descriptive'),
        ),
        migrations.AddField(
            model_name='activite',
            name='titre',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Titre'),
        ),
    ]