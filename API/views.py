

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserSettings
import json
from django.core import serializers
from django.middleware import csrf
from rest_framework.authentication import BasicAuthentication
from .wmigbot import WMIGBot
from .models import Dispensary, UserSettings
from django.contrib.auth.decorators import login_required



# Create your views here.

def check_login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return True
    else:
        return False


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


class Logout(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request):
        logout(request)
        msg = "User logged out"
        return Response({"message": msg})


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

    authentication_classes = [BasicAuthentication]

    def get(self, request):
        if check_login(request):
            print(request.user)
            data = {"message": "User authenticated"}
        else:
            data = {"message": "Not authenticated"}
        return Response(data)

    def post(self, request):
        num = int(request.data['num'])
        response = {'num': num + 1}
        return Response(response)


class Instagrams(APIView):

    authentication_classes = [BasicAuthentication]

    def post(self, request, id):

        if check_login(request):
            igusername = request.data['igusername']
            igpassword = request.data['igpassword']
            userSettings = UserSettings.objects.get(userID=id)
            userSettings.igUsername = igusername
            userSettings.igPassword = igpassword
            userSettings.save()
            msg = "Instagram credentials logged"

        else:
            msg = "You are not logged in."
        resp = {"message": msg}
        return Response(resp)


class WMs(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request, id):
        user_settings = UserSettings.objects.get(userID=id)
        data = serializers.serialize("json", [user_settings])
        return Response(data)


    def post(self, request, id):
        if check_login(request):
            url = request.data['url']
            try:
                dispensary = Dispensary.objects.get(url=url)
                settings = UserSettings.objects.get(userID=id)
                settings.weedmapsSlug = dispensary.slug
                settings.save()
                msg = "Assigned Weedmaps Menu"
            except Exception:
                msg = "Not a valid URL"
        else:
            msg = "Not logged in"

        return Response({"message": msg})


class Settings(APIView):

    authentication_classes = [BasicAuthentication]

    def get(self, request, id):

        try:
            user_settings = UserSettings.objects.get(userID=id)
            msg = "Settings Found"
            data = serializers.serialize("json", [user_settings, {'message': msg}])
            print(data)




        except Exception:
            msg = "Settings not found"
            data = {"message": msg}

        return Response(data)

    def post(self, request, id):
        if check_login(request):
            memeOn = request.data['memesOn']
            dailyDealsOn = request.data['dailyDealsOn']
            newItemsOn = request.data['newItemsOn']
            user_settings = UserSettings.objects.get(userID=id)
            user_settings.memeOn = memeOn
            user_settings.newMenuItemsOn = newItemsOn
            user_settings.dailyDealsOn = dailyDealsOn
            user_settings.save()
            resp = {"message": "Settings were updated"}
        else:
            resp = {"message": "Not logged in"}
        return Response(resp)


class BotRun(APIView):

    def post(self, request, userID):

        if check_login(request):
            settings = UserSettings.objects.get(userID=request.user.id)
            if settings.botStatus == False:
                bot = WMIGBot(userID)
                bot.run()
                resp = {"message": "Bot is now running"}
            else:
                resp = {"message": "Bot is already running"}

        else:
            resp = {"message": "Not Logged in"}
        return Response(resp)

class BotStop(APIView):

    def post(self, request, userID):
        if check_login(request):
            print(request.user.id)
            bot = WMIGBot(userID)
            bot.stop()
            settings = UserSettings.objects.get(userID=request.user.id)
            settings.botStatus = False
            settings.save()
            resp = {"message": "Bot has been stopped"}
        else:
            resp = {"message": "Not logged in"}
        return Response(resp)

class BotTest(APIView):

    authentication_classes = [BasicAuthentication]

    def post(self, request, userID):
        if check_login(request):
            bot = WMIGBot(userID)
            bot.test()
            resp = {"message", "It should have posted"}
        else:
            resp = {"message": "Not logged in"}
        return Response(resp)







# scrape dispensaries.  Ask users for url of WM page to match in database. Slug and tipe will be found.




