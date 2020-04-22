from django.db import models
from django.contrib.auth.models import User
from.choices import *

import datetime

# Create your models here.
# Theses models should mirror the database schema design

class Character(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    Subclass = models.CharField(max_length=30)
    Name = models.CharField(max_length=15)
    def __str__(self):
        return self.Name

class HellRuns(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    Date = models.DateField(default=datetime.date.today)
    HellType = models.CharField(
        max_length=2,
        choices=HELL_TYPE_CHOICES,
        default=GUIDE_OF_WISDOM
    )
    Runs = models.IntegerField(default=1) # at least 1 run must be done per entry
    StoneBox = models.IntegerField(default=0)
    EpicSoul = models.IntegerField(default=0)
    EpicDrops = models.IntegerField(default=0)


