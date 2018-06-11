import peewee
import sqlite3
import json
import urllib.request
from .models import Dispensary


conn = sqlite3.connect("/Users/Hallshit/Documents/MGIGBOT/venv/IGBOTAPIVENV/IGBOTAPI/db.sqlite3")

c = conn.cursor()

def downloadDispensaries():
    deliveryDisURL = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=san-francisco&page_size=100&size=100'
    dispensaries = json.loads(urllib.request.urlopen(deliveryDisURL).read().decode('utf-8'))['data']['listings']
    print(dispensaries)
    for d in dispensaries:
        dispensary = Dispensary(slug=d['slug'], url=d['web_url'], tipe=d['type'])
        dispensary.save()









