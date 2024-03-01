from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=100, blank=True)
    firstname = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    dob = models.DateField(blank=True, null=True)
    number = models.CharField(max_length=13, blank=True)
    profile_pic = models.ImageField(default='empty_avatar.jpg', upload_to='profile')

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_age(self):
        curr_year = datetime.now().year
        curr_month = datetime.now().month

        diff = curr_year - self.dob.year 
        if self.dob.month > curr_month:
            return diff - 1
        return diff