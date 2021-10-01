from django.db import models
from person_app.models import PersonDB
from sport_type_app.models import SportTypeDB
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CoachDB(models.Model):
    person = models.OneToOneField(PersonDB, on_delete=models.CASCADE, related_name='coach_detail')
    fav_sport = models.ManyToManyField(SportTypeDB)
    raiting = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)],blank=True)
    description = models.CharField(max_length=255,blank=True)

    # todo:
    # post_id , practice
    def __str__(self):
        return self.person.first_name
