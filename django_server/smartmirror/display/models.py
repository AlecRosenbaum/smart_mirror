import uuid

from django.db import models
from accounts.models import UserProfile

# models used to save display options
# class Calendar(models.Model):
#     user = models.ForeignKey(UserProfile)
#     link = models.CharField(max_length=256) 

# class Mirror(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(UserProfile)
#     name = models.CharField(max_length=50, default="User's Mirror") 

class ShortMirror(models.Model):
    user = models.ForeignKey(UserProfile)
    short_id = models.CharField(max_length=5)

    def __str__(self):
        return self.user.user.first_name + " " + self.user.user.last_name + " " + self.short_id