# Generated by Django 5.0.2 on 2024-03-05 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0005_rename_profile_scolaire_profiles_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='commune',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mentors.communes'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='domaine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mentors.categorieformation'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='niveau',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profiles',
            name='ojectif',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profiles',
            name='type_mentorat',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
