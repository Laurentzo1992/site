# Generated by Django 5.0.2 on 2024-08-25 23:07

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0005_delete_mailpersonalise_mentor_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activite',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Description'),
        ),
    ]