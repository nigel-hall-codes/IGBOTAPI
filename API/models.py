from django.db import models

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






# Can get weedmaps slug through url


