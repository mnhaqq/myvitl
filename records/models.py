from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temperature = models.FloatField()
    heart_rate = models.PositiveIntegerField()
    sugar_level = models.PositiveIntegerField()
    date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user.username}'s record on {self.date}"
    
    def get_date(self):
        return self.date.strftime('%b %d, %Y')
    
    def get_time(self):
        return self.date.strftime('%I:%M %p')
    
    