# Generated by Django 3.2.7 on 2021-11-19 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location_app', '0002_auto_20211119_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationdb',
            old_name='lng',
            new_name='long',
        ),
        migrations.AlterUniqueTogether(
            name='locationdb',
            unique_together=set(),
        ),
    ]
