# Generated by Django 3.2.7 on 2021-10-16 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainee_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traineedb',
            name='fav_sport',
        ),
    ]
