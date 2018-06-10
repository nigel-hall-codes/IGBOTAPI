

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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

