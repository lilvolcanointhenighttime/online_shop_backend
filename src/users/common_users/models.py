from django.db import models

# Create your models here.

class CommonUser(models.Model):
    username = models.CharField(max_length=64, unique=True)
