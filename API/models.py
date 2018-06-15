from django.db import models
import json
import urllib.request

# Create your models here.


from django.db import models


class UserSettings(models.Model):

    userID = models.IntegerField()
    memeOn = models.BooleanField(default=True)
    newMenuItemsOn = models.BooleanField(default=True)
    dailyDealsOn = models.BooleanField(default=True)
    igUsername = models.TextField(default="Not given")
    igPassword = models.TextField(default="Not given")
    weedmapsSlug = models.TextField(default="Not given")
    botPID = models.IntegerField(default=0)
    botStatus = models.BooleanField(default=False)


class MenuItem(models.Model):

    dispensaryID = models.IntegerField()
    dateAdded = models.DateTimeField()
    name = models.TextField()
    prices = models.TextField()


class Dispensary(models.Model):

    wmid = models.IntegerField(default=0)
    slug = models.TextField()
    url = models.TextField()
    tipe = models.TextField(default="dispensary")




