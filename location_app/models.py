from django.db import models
from django.utils.text import slugify

from person_app.models import PersonDB
from coach_app.models import CoachDB


class CountryDB(models.Model):
    name = models.CharField(max_length=120, unique=True)
    # long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # place_id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class CityDB(models.Model):
    country = models.ForeignKey(CountryDB, on_delete=models.CASCADE, related_name='city_location')
    name = models.CharField(max_length=120)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    place_id = models.CharField(max_length=100, primary_key=True)

    class Meta:
        unique_together = ('country', 'name',)

    def __str__(self):
        return self.name


# Create your models here.
class LocationDB(models.Model):
    coach = models.ForeignKey(CoachDB, on_delete=models.CASCADE, related_name='location')
    # country = models.ForeignKey(CountryDB, on_delete=models.CASCADE, related_name='location_country')
    city = models.ForeignKey(CityDB, on_delete=models.CASCADE, related_name='location_city')
    # todo: when doing the map add lat long
    # place_id = models.CharField(max_length=100, primary_key=True)
    # long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.coach.person.first_name + ' ' + self.coach.person.last_name + ' city: ' + self.city

