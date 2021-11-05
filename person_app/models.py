from django.db import models
from abc import ABC, abstractmethod
from sport_type_app.models import SportTypeDB
from phonenumber_field.modelfields import PhoneNumberField

# from trainee_app.models import TraineeDB
from user_app.models import UserDB
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class PersonDB(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('D', 'Different'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(unique=False, max_length=100)
    last_name = models.CharField(unique=False, max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = PhoneNumberField(blank=True)
    is_coach = models.BooleanField(default=False)
    fav_sport = models.ManyToManyField(SportTypeDB)
    profile_image = models.URLField(null=True,
                                    blank=True,
                                    default="https://www.essd.eu/wp-content/uploads/2020/07/ESSD_Hungary-12.jpg")

    def __str__(self):
        return self.first_name + " " +self.last_name