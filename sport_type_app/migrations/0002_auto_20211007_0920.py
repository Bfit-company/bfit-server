# Generated by Django 3.2.7 on 2021-10-07 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport_type_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sporttypedb',
            old_name='raiting',
            new_name='rating',
        ),
        migrations.AddField(
            model_name='sporttypedb',
            name='sport_image',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
    ]
