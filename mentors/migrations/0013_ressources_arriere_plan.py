# Generated by Django 5.0.2 on 2024-03-05 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0012_slideimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='ressources',
            name='arriere_plan',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
