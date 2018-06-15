import sqlite3
import json
import urllib.request
import os, sys
import django

sys.path.append(os.path.join(sys.path[0], '../../'))

sys.path.append("/Users/Hallshit/Documents/MGIGBOT/venv/IGBOTAPIVENV/IGBOTAPI/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IGBOTSITE.settings")
django.setup()

from API.models import Dispensary

southCity = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=doctors&filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=south-san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=south-san-francisco&filter%5Bregion_slug%5Bdoctors%5D%5D=san-francisco&page_size=100&size=100'
sanFran = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=san-francisco&page_size=100&size=100'

def downloadDispensaries():
    deliveryDisURL = southCity
    dispensaries = json.loads(urllib.request.urlopen(deliveryDisURL).read().decode('utf-8'))['data']['listings']
    # print(dispensaries)
    for d in dispensaries:
        dispensary, create = Dispensary.objects.get_or_create(slug=d['slug'], url=d['web_url'], tipe=d['type'], wmid=d['wmid'])
        dispensary.save()






