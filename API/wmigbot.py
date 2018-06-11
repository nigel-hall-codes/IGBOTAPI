import os
import sys
import time
import schedule
from io import open
from instabot import Bot
from getMenu import Menu
import urllib.request
import json
from PIL import Image
import datetime
from .models import Dispensary

sys.path.append(os.path.join(sys.path[0], '../../'))


class WMIGBot:
    def __init__(self, igusername, igpassword, wmURL):
        self.igusername = igusername
        self.igpassword = igpassword
        self.wmURL = wmURL

    def post_meme(self):
        bot = Bot()
        bot.login(username=self.igusername, password=self.igpassword)
        memes = bot.get_hashtag_medias("funnyweed")
        posted_memes = open("postedMemes.txt", "r").read().splitlines()

        for m in memes:
            if str(m) not in posted_memes:
                try:
                    bot.download_photo(m, filename=m, folder="memesToBeUploaded")
                    op =  bot.get_media_info(m)[0]['user']['username']
                    bot.upload_photo('memesToBeUploaded/{}.jpg'.format(m),
                                      caption="Credits to @{}".format(op))
                    os.remove('memeToBeUploaded/{}.jpg'.format(m))
                    f = open('postedMemes.txt', 'a')
                    f.write(str(m) + '\n')
                    f.close()
                    break

                except Exception as e:
                    bot.logger.warning("Download Failed")
                    print("Download Failed ", e)

        bot.logout()

    def post_new_menu_items(self):
        dispensary = Dispensary.objects.get(url=self.wmURL)
        m = Menu(dispensary.slug, dispensary.tipe)
        m.downloadNewMenuItemImages()







