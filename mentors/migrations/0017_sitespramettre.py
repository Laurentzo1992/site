# Generated by Django 5.0.2 on 2024-03-24 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0016_evenement_lien'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitesPramettre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.FileField(blank=True, null=True, upload_to='images/')),
                ('nom_site', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
