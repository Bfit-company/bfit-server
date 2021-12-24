# Generated by Django 3.2.9 on 2021-12-22 22:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coach_app', '0010_alter_coachdb_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachdb',
            name='rating',
            field=models.FloatField(blank=True, default=3, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(1.0)]),
        ),
    ]
