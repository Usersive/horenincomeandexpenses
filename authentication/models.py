from django.db import models
from django.contrib.auth.models import User 
from django.utils.timezone import now
# Create your models here.




class Profile(models.Model):
    GENDER_CHOICES =(
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    profile_image = models.ImageField(default='default_profile.png', upload_to='profile_pics')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile_details = models.CharField(max_length=450)
    date = models.DateField(default=now)

    def _str_(self):
        return self.name

class About(models.Model):
    about_us = models.TextField(max_length=500)
    
    def _str_(self):
        return self.about_us