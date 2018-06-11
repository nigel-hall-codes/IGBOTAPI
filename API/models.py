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


class MenuItem(models.Model):

    dispensaryID = models.IntegerField()
    dateAdded = models.DateTimeField()
    name = models.TextField()
    prices = models.TextField()


class Dispensary(models.Model):

    slug = models.TextField()
    url = models.TextField()
    tipe = models.TextField(default="dispensary")







# Can get weedmaps slug through url


# Helper functions

# def downloadDispensaries():
#     deliveryDisURL = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=san-francisco&page_size=100&size=100'
#     dispensaries = json.loads(urllib.request.urlopen(deliveryDisURL).read())['data']['listings']
#     for d in dispensaries:
#         dispensary = Dispensary(slug=d['slug'], url=d['url'])
#         dispensary.save()
#
#
#



