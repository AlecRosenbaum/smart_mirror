from django.db import models
from accounts.models import UserProfile

# models used to save display options
class Calendar(models.Model):
    user = models.ForeignKey(UserProfile)
    time_zone = models.CharField(max_length=30, default='America/New_York') 

class Mirror(models.Model):
    user = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=50, default="User's Mirror") 
