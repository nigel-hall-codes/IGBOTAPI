import sqlite3
import json
import urllib.request
import os, sys
import django

sys.path.append(os.path.join(sys.path[0], '../../'))

sys.path.append("/Users/Hallshit/Documents/MGIGBOT/venv/IGBOTAPIVENV/IGBOTAPI/")
sys.path.append("/var/www/IGBOTProject3/IGBOTAPI")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IGBOTSITE.settings")
django.setup()

from API.models import Dispensary

southCity = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=doctors&filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=south-san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=south-san-francisco&filter%5Bregion_slug%5Bdoctors%5D%5D=san-francisco&page_size=100&size=100'
sanFran = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=san-francisco&page_size=100&size=100'

# def downloadDispensaries():
#     deliveryDisURL = southCity
#     dispensaries = json.loads(urllib.request.urlopen(deliveryDisURL).read().decode('utf-8'))['data']['listings']
#     # print(dispensaries)
#     for d in dispensaries:
#         dispensary, create = Dispensary.objects.get_or_create(slug=d['slug'], url=d['web_url'], tipe=d['type'], wmid=d['wmid'])
#         dispensary.save()



def download_dispensaries():
    url1 = "https://api-g.weedmaps.com/wm/v2/listings?filter%5Bbounding_box%5D=37.76786513360663,-122.48150825500488,37.81127577036112,-122.39001274108888&filter%5Bplural_types%5D%5B%5D=doctors&filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&page_size=100&size=100"
    url2 = "https://api-g.weedmaps.com/wm/v2/listings?filter%5Bbounding_box%5D=37.67376658565116,-122.64484405517578,37.86130199456176,-122.36743927001952&filter%5Bplural_types%5D%5B%5D=doctors&filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&page_size=100&size=100"
    url3 = "https://api-g.weedmaps.com/wm/v2/listings?filter%5Bbounding_box%5D=37.68803162408617,-122.57600784301756,37.781840715520495,-122.40726470947266&filter%5Bplural_types%5D%5B%5D=doctors&filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&page_size=100&size=100"
    url4 = "https://api-g.weedmaps.com/wm/v2/listings?filter%5Bbounding_box%5D=37.62483706088789,-122.56605148315428,37.71180059181106,-122.37464904785155&filter%5Bplural_types%5D%5B%5D=doctors&filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&page_size=100&size=100"
    urls = [url1, url2, url3, url4]

    for url in urls:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))['data']
        listings = data['listings']
        for l in listings:
            l_dict = {}

            l_dict['tipe'] = l['type']
            l_dict['slug'] = l['slug']
            l_dict['wmid'] = l['wmid']
            print(l_dict)
            d, created = Dispensary.objects.get_or_create(**l_dict)




