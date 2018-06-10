from django.db import models

# Create your models here.


from django.db import models

class UserSettings(models.Model):
    userID = models.IntegerField()
    memeOn = models.BooleanField()
    newMenuItemsOn = models.BooleanField()
    dailyDealsOn = models.BooleanField()
    igUsername = models.TextField()
    igPassword = models.TextField()
    weemapsSlug = models.TextField()


# Can get weedmaps slug through url


