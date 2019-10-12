from __future__ import unicode_literals
from django.db import models
class UserInfo (models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
# Create your models here.
