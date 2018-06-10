

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserSettings


# Create your views here.

def home(request):
    return render(request, 'home.html')


class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            message = "Logged in as {}".format(username)
        else:
            message = "Incorrect username or password"
        data = {"message": message}
        return Response(data)


class CreateUser(APIView):
    def post(self, request):
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        user = User.objects.create_user(username, email, password)

        userSettings = UserSettings(userID=user.id)
        userSettings.save()
        resp = {"message": "User created"}
        return Response(resp)


class testAPI(APIView):
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

class AddIGCredentials(APIView):
    def post(self, request):
        username = request.data['user']
        igusername = request.data['igusername']
        igpassword = request.data['igpassword']
        user = User.objects.get(username=username)
        userSettings = UserSettings.objects.get(userID=user.id)
        userSettings.igUsername = igusername
        userSettings.igPassword = igpassword
        userSettings.save()
        resp = {"message": "Instagram verified"}
        return Response(resp)


class AddWeedmapsPage(APIView):
    def post(self, reques):
        pass


# scrape dispensaries.  Ask users for url of WM page to match in database. Slug and tipe will be found.




