# Generated by Django 5.0.2 on 2024-03-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0019_presentation_delete_sitespramettre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='valeur',
        ),
        migrations.AlterField(
            model_name='presentation',
            name='nom_site',
            field=models.CharField(blank=True, default='OSER', max_length=200, null=True),
        ),
    ]
