# Generated by Django 5.0.2 on 2024-03-06 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0015_evenement_date_even'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='lien',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
