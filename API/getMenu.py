import urllib.request
import json
import django
import sys, os
import time
sys.path.append("/Users/Hallshit/Documents/MGIGBOT/venv/IGBOTAPIVENV/IGBOTAPI/")
sys.path.append("/var/www/IGBOTProject3/IGBOTAPI")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IGBOTSITE.settings")
django.setup()

from API.models import MenuItem, Dispensary
import datetime
from PIL import Image

class Menu:
    def __init__(self, slug, tipe):
        url = 'https://api-g.weedmaps.com/wm/web/v1/listings/{}/menu?type={}'.format(slug, tipe)
        page = urllib.request.urlopen(url)
        # print(page.read())
        data = json.loads(page.read().decode('utf-8'))
        self.data = data
        self.categories = data['categories']
        self.items = []
        self.dispensary = Dispensary.objects.get(slug=slug)

        for c in self.categories:
            for i in c['items']:
                # print(i)
                obj = {}
                obj['name'] = i['name']
                obj['category'] = i['category_name']
                obj['prices'] = i['prices']
                obj['url'] = i['image_url']
                self.items.append(obj)

    def downloadMenu(self):
        t = datetime.datetime.now()
        for i in self.items:
            m = MenuItem(dateAdded=t,
                         dispensaryID=self.dispensary.id,
                         name=i['name'],
                         prices=str(i['prices']),
                         )
            m.save()

    def newMenuItems(self):
        lastDate = MenuItem.objects.last().dateAdded
        lm = MenuItem.objects.filter(dateAdded=lastDate)
        lastMenuNames = [i.name for i in lm]
        currentMenuNames = [i['name'] for i in self.items]
        return [name for name in currentMenuNames if name not in lastMenuNames]

    def downloadNewMenuItemImages(self, base_dir):

        for i in self.items:
            if i['name'] in self.newMenuItems():
                fmt = i['url'].split('.')[-1]
                urllib.request.urlretrieve(i['url'], '{}{}.{}'.format(base_dir, i['name'], fmt))
                if fmt == 'png':
                    img = Image.open('{}{}.{}'.format(base_dir, i['name'], fmt))
                    rgb_im = img.convert('RGB')
                    rgb_im.save('{}{}.jpg'.format(base_dir, i['name']))
        self.downloadMenu()

    def downloadDailyDealImage(self, url, t, base_dir):
        fmt = url.split(".")[-1]
        name = t
        urllib.request.urlretrieve(url, '{}{}.{}'.format(base_dir, name, fmt))
        if fmt == 'png':
            img = Image.open('{}{}.{}'.format(base_dir, name, fmt))
            rgb_im = img.convert('RGB')
            rgb_im.save('{}{}.jpg'.format(base_dir, name))

    def todays_deal(self):
        return self.data['listing']['todays_deal']



# print(m.newMenuItems())












