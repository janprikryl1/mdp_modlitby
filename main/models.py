from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Politician(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=25)
    position = models.CharField(max_length=35)

    intercessors = models.ManyToManyField(User)# Přímluvci

    def __str__(self):
        return self.name + self.surname