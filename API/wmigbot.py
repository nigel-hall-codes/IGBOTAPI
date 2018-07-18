import os
import sys
import time
import schedule
from io import open
from instabot import Bot

import urllib.request
import json
from PIL import Image
import datetime
import os
import django
import subprocess
sys.path.append(os.path.join(sys.path[0], '../../'))

sys.path.append("/Users/Hallshit/Documents/MGIGBOT/venv/IGBOTAPIVENV/IGBOTAPI/")
sys.path.append("/var/www/IGBOTProject3/IGBOTAPI")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IGBOTSITE.settings")
django.setup()

# {"username": "newaccount", "password": "newaccount"}

from API.models import UserSettings, MenuItem, Dispensary
from API.getMenu import Menu


class WMIGBot:
    def __init__(self, userID):
        self.userID = userID
        self.settings = UserSettings.objects.get(userID=self.userID)
        self.igusername = self.settings.igUsername
        self.igpassword = self.settings.igPassword
        self.wm_slug = self.settings.weedmapsSlug
        self.accountDir = "accounts/{}".format(self.igusername)
        self.initialize_directory()
        self.dispensary = Dispensary.objects.get(slug=self.wm_slug)

    def initialize_directory(self):
        if not os.path.exists(self.accountDir):
            os.makedirs(self.accountDir)
            f = open("{}/postedMemes.txt".format(self.accountDir), "w+")
            f.close()
            os.makedirs("{}/memesToBeUploaded".format(self.accountDir))
            os.makedirs("{}/menuItemsToBeUploaded".format(self.accountDir))
            os.makedirs("{}/dailyDealsToBeUploaded".format(self.accountDir))


    def post_meme(self):
        self.settings = UserSettings.objects.get(userID=self.userID)
        if self.settings.memeOn:
            bot = Bot()
            bot.login(username=self.igusername, password=self.igpassword)
            memes = bot.get_hashtag_medias("420")
            posted_memes = open("{}/postedMemes.txt".format(self.accountDir), "r").read().splitlines()

            for m in memes:
                if str(m) not in posted_memes:
                    try:
                        bot.download_photo(m, filename=m, folder="{}/memesToBeUploaded".format(self.accountDir))
                        op = bot.get_media_info(m)[0]['user']['username']
                        bot.upload_photo('{}/memesToBeUploaded/{}.jpg'.format(self.accountDir, m),
                                          caption="Credits to {}".format(op))
                        os.remove('{}/memesToBeUploaded/{}.jpg'.format(self.accountDir, m))
                        f = open('{}/postedMemes.txt'.format(self.accountDir), 'a')
                        f.write(str(m) + '\n')
                        f.close()
                        break

                    except Exception as e:
                        bot.logger.warning("Download Failed")
                        print("Download Failed ", e)
            bot.logout()

    def run(self):
        path = os.getcwd()
        bash = "nohup python3 {}/API/wmigbot.py {} {} &> {}.out& ".format(path,
                                                                         str(self.userID),
                                                                         "False",
                                                                         path + "/API/" + self.accountDir + "/alt"
                                                                        )
        print(bash)


        # p = subprocess.Popen(["python3", path+"/API/wmigbot.py", str(self.userID), "False"])
        p = subprocess.Popen(bash.split(" "))
        self.settings.botPID = p.pid
        self.settings.botStatus = True
        self.settings.save()
        print("Bot Started: PID={}".format(p.pid))

    def stop(self):
        pid = self.settings.botPID
        subprocess.Popen(["kill", "-9", str(pid)])
        self.settings.botStatus = False
        self.settings.save()
        print("Bot destroyed")

    def post_new_menu_items(self):
        self.settings = UserSettings.objects.get(userID=self.userID)
        if self.settings.newMenuItemsOn:
            m = Menu(self.dispensary.slug, self.dispensary.tipe)
            base_dir = self.accountDir + "/menuItemsToBeUploaded/"
            m.downloadNewMenuItemImages(base_dir)
            bot = Bot()
            bot.login(username=self.igusername, password=self.igpassword)
            for image in os.listdir(self.accountDir + '/menuItemsToBeUploaded'):
                name = "".join(image.split('.')[:-1])
                bot.upload_photo('{}{}'.format(base_dir, image),
                                 caption="We just added a new item to our menu on Weedmaps! {}".format(name))
                os.remove('{}{}'.format(base_dir, image))
            print("new Menu Downloaded")
            bot.logout()

    def post_daily_deal(self):
        self.settings = UserSettings.objects.get(userID=self.userID)
        if self.settings.dailyDealsOn:
            time = datetime.datetime.now()
            base_dir = self.accountDir + "/dailyDealsToBeUploaded/"
            bot = Bot()
            bot.login(username=self.igusername, password=self.igpassword)
            m = Menu(self.dispensary.slug, self.dispensary.tipe)
            todays_deal = m.todays_deal()
            caption = "Check out today's deal: " + todays_deal['title']
            imageURL = todays_deal['picture_urls']['medium']
            m.downloadDailyDealImage(imageURL, time, base_dir)
            bot.upload_photo("{}{}.jpg".format(base_dir, time), caption=caption)
            os.remove("{}{}.jpg".format(base_dir, time))

    def test(self):
        path = os.getcwd()
        p = subprocess.Popen(["python3", path + "/API/wmigbot.py", str(self.userID), "True"])
        self.settings.botPID = p.pid
        self.settings.botStatus = True
        self.settings.save()
        print("Bot Started")



if __name__ == '__main__':

    bot = WMIGBot(sys.argv[1])

    if eval(sys.argv[2]):
        print("Tested at {}".format(datetime.datetime.now()))
        bot.post_meme()

    else:
        print("Bot started on {}".format(datetime.datetime.now()))
        schedule.every().day.at("00:08").do(bot.post_new_menu_items)
        schedule.every().day.at("00:08").do(bot.post_daily_deal)
        schedule.every(6).hours.do(bot.post_meme)
        # schedule.every().day.at("23:31").do(bot.post_meme)

        while True:

            schedule.run_pending()
            print(bot.settings.botPID)
            time.sleep(60)



