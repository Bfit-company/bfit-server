from django.db import models
from person_app.models import PersonDB
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CoachDB(models.Model):
    person = models.OneToOneField(PersonDB, on_delete=models.CASCADE, related_name='coach_detail')
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)],blank=True,default=1)
    description = models.CharField(max_length=255,blank=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)

    # todo:
    # post_id , practice
    def __str__(self):
        return self.person.first_name
