from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    context = {}
    return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

def test(request):
    context = {}
    return render(request, 'djangoapp/test.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    print("request", request)
    for key in request: 
        print(key)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            print(111111111)
            login(request, user)
            return redirect('djangoapp:index')
            
        else:
            print(2222222)
            context['message'] = "Invalid username or password."
            return redirect('djangoapp:registration_request')
    else:
        print(33333333)
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    print("request", request)
    context = {}
    if request.method == 'GET':
        print("BBBBBBBB")
        form = UserCreationForm()
        context['form']=form
        return render(request, 'djangoapp/signup.html', context)
    elif request.method == 'POST':
        # Check if user exists
        print("AAAAAAAAA")
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            print(44444444)
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            print(555555555)
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

