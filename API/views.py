

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserSettings
import json
from django.core import serializers
from django.middleware import csrf
from rest_framework.authentication import BasicAuthentication
from .wmigbot import WMIGBot
from .models import Dispensary, UserSettings

import subprocess
import asyncio



# Create your views here.

def home(request):
    return render(request, 'home.html')


class Login(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request):
        token = csrf.get_token(request)
        resp = {"token": token}
        return Response(resp)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            message = "Logged in as {}".format(username)
        else:
            message = "Incorrect username or password"
        data = {"message": message, "userID": user.id}
        return Response(data)


class Create(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request):
        resp = {"message": "Need to do POST req"}
        return Response(resp)

    def post(self, request):
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        # Check if doesnt exist

        user = User.objects.create_user(username, email, password)
        user_settings = UserSettings(userID=user.id)
        user_settings.save()

        resp = {"message": "User created"}
        return Response(resp)


class TestAPI(APIView):

    def get(self, request):
        data = {"message": "Hello Carlos"}
        return Response(data)

    def post(self, request):
        num = int(request.data['num'])
        response = {'num': num + 1}
        return Response(response)


class MemesOn(APIView):

    def post(self, request):
        on = request.data["on"]
        print(type(on))
        if type(on) == type(1):
            print("Set option")
            response = {"message": "Option has been set"}

        else:
            print("Not a bool")
            response = {"message": "Not a Bool"}

        return Response(response)


class NewDealsOn(APIView):
    def post(self, request):
        on = request.data["on"]
        if type(on) == type(1):
            response = {"message": "Option has been set"}
        else:
            response = {"message": "Not a Bool"}
        return Response(response)

class Instagrams(APIView):
    authentication_classes = [BasicAuthentication]
    def post(self, request, id):
        igusername = request.data['igusername']
        igpassword = request.data['igpassword']
        userSettings = UserSettings.objects.get(userID=id)
        userSettings.igUsername = igusername
        userSettings.igPassword = igpassword
        userSettings.save()
        resp = {"message": "Instagram verified"}
        return Response(resp)


class WMs(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request, id):
        user_settings = UserSettings.objects.get(userID=id)
        data = serializers.serialize("json", [user_settings])
        return Response(data)


    def post(self, request, id):
        url = request.data['url']
        dispensary = Dispensary.objects.get(url=url)
        settings = UserSettings.get(userID=id)
        settings.weedmapsSlug = dispensary.wmid
        settings.save()
        resp = {"message": "Assigned Weedmaps Menu"}



class Settings(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request, id):
        user_settings = UserSettings.objects.get(userID=id)
        data = serializers.serialize("json", [user_settings])
        return Response(data)

    def post(self, request, id):
        memeOn = request.data['memesOn']
        dailyDealsOn = request.data['dailyDealsOn']
        newItemsOn = request.data['newItemsOn']
        user_settings = UserSettings.objects.get(userID=id)
        user_settings.memeOn = memeOn
        user_settings.newMenuItemsOn = newItemsOn
        user_settings.dailyDealsOn = dailyDealsOn
        user_settings.save()
        resp = {"message": "Settings were updated"}
        return Response(resp)


class BotRun(APIView):

    def get(self, request, userID):
        # If bot already running ignore.  Set status to on in db
        settings = UserSettings.objects.get(userID=userID)
        if settings.botStatus == False:
            bot = WMIGBot(userID)
            bot.run()
            resp = {"message", "Bot is now running"}
        return Response(resp)

class BotStop(APIView):

    def get(self, request, userID):
        bot = WMIGBot(userID)
        bot.stop()
        resp = {"message", "Bot has been stopped"}
        return Response(resp)

class BotTest(APIView):

    def get(self, request, userID):
        print(userID)
        bot = WMIGBot(userID)
        bot.test()
        resp = {"message", "It should have posted"}
        return Response(resp)





# scrape dispensaries.  Ask users for url of WM page to match in database. Slug and tipe will be found.




