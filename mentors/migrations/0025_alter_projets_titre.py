# Generated by Django 5.0.2 on 2024-03-26 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0024_projets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projets',
            name='titre',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
