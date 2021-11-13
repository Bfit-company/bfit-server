from django.db import models
from django.utils.text import slugify

from person_app.models import PersonDB
from coach_app.models import CoachDB
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class LocationDB(models.Model):
    coach = models.ForeignKey(CoachDB, on_delete=models.CASCADE, related_name='location')
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)

    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.coach.person.first_name + ' ' + self.coach.person.last_name + ' city: ' + self.city
