# Generated by Django 5.0.2 on 2024-03-05 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0011_alter_profiles_niveau'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slideimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/')),
                ('titre1', models.CharField(blank=True, max_length=200, null=True)),
                ('titre2', models.CharField(blank=True, max_length=200, null=True)),
                ('titre3', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
