# Generated by Django 3.2.7 on 2021-10-30 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0002_remove_postdb_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postdb',
            name='slug',
        ),
    ]