# Generated by Django 5.0.2 on 2025-05-11 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0006_forumcomment_comment_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumcomment',
            name='comment_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='forumcomment',
            name='comment_views',
            field=models.IntegerField(default=0),
        ),
    ]
