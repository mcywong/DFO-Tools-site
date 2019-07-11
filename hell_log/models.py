from django.db import models
from.choices import *

import datetime

# Create your models here.
# Theses models should mirror the database schema design

class Account(models.Model):
    username = models.CharField(max_length=30) #Double check username character limit in game
    def __str__(self):
        return self.username

class Character(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    subclass = models.CharField(max_length=30)
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class HellRuns(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    Date = models.DateField(default=datetime.date.today)
    HellType = models.CharField(
        max_length=2,
        choices=HELL_TYPE_CHOICES,
        default=HARLEM_HELL
    )
    Runs = models.IntegerField(default=1) # at least 1 run must be done per entry
    HellOrb = models.IntegerField(default=0)
    StoneBox = models.IntegerField(default=0)
    EpicSoul = models.IntegerField(default=0)
    EpicDrops = models.IntegerField(default=0)
    SkyFrags = models.IntegerField(default=0)
    AntimatterParticle = models.IntegerField(default=0)

