from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .restapis import get_dealers_from_cf, get_dealers_by_id, get_dealers_by_state, post_review, get_reviews_from_cf,get_dealer_name_from_id
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import copy
import random
from .models import Certificate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def general(request):
    context = {"title": "Overview"}
    return render(request, 'djangoapp/general.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {"title":"Contact"}
    return render(request, 'djangoapp/contact.html', context)

def resumee(request):
    context = {"title": "My Resumee",
               'image': 'photoCV haute resolution_cropped.png'}
    return render(request, 'djangoapp/resumee.html', context)

def comments(request):
    context = {"title": "Comments",
               'image': 'chat.png'}
    return render(request, 'djangoapp/comments.html', context)

def certificates(request):

    context = {"title": "My Certificates and Diplomas",
               'image': 'diplomas-hat.jpg',
               'certifs':[]}
    if request.method == "GET":

        certifs = Certificate.objects.all()
        for i, certif in enumerate(certifs):
            certificate_json = {
                "title": certif.title,
                "school": certif.school,
                "topics": certif.get_topics(),
                "skills": certif.get_skills(),
                "link1": certif.link,
                "link2": certif.link2,
            }
            context["certifs"].append(certificate_json)
        # print(context)
    elif request.method == "POST":
        if (len(request.POST)==1 or "all" in request.POST):
            certifs = Certificate.objects.all()
            for i, certif in enumerate(certifs):
                certificate_json = {
                    "title": certif.title,
                    "school": certif.school,
                    "topics": certif.get_topics(),
                    "skills": certif.get_skills(),
                    "link1": certif.link,
                    "link2": certif.link2,
                }
                context["certifs"].append(certificate_json)
                context["skills"] = 1 # To have context["skills"] evaluated to True in order to have  an automatic scroll
        else:
            print("POST_REQUEST_TEST", request.POST)
            flags = []
            for flag in request.POST:
                flags.append(flag)
            print("flags",flags)

            context["flags"]=flags[1:]
            # print(context)

            certifs = 0

            for flag in flags[1:]:
                print("certifs", certifs)
                if certifs == 0:
                    certifs = Certificate.objects.filter(flags__contains = flag)
                else:
                    certifs= certifs | (Certificate.objects.filter(flags__contains = flag))
            for i, certif in enumerate(certifs):
                certificate_json = {
                    "title": certif.title,
                    "school": certif.school,
                    "topics": certif.get_topics(),
                    "skills": certif.get_skills(),
                    "link1": certif.link,
                    "link2": certif.link2,
                }
                context["certifs"].append(certificate_json)

    return render(request, 'djangoapp/certificates.html', context)

def gallery(request):
    context = {"title": "Gallery",
               "image": "Art.jpg"}
    return render(request, 'djangoapp/gallery.html', context)

def minigame(request):
    context = {"title": "Mini Game"}
    return render(request, 'djangoapp/minigame.html', context)



def test(request):
    context = {}
    return render(request, 'djangoapp/test.html', context)

def dealerships(request):
    context = {}
    if request.method == "POST":
        if request.POST['dealerId']:
            dealerId = request.POST['dealerId']
            url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/dealership"
            # Get dealers from the URL
            dealerships = get_dealers_by_id(url, dealerId=dealerId)
            print(dealerships)
            context["dealerships"]=dealerships
        else:
            state = request.POST['state']
            url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/dealership"
            # Get dealers from the URL
            dealerships = get_dealers_by_state(url, state=state)
            print(dealerships)
            context["dealerships"]=dealerships

    return render(request, 'djangoapp/dealerships.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    print("request", request)
    for key in request: 
        print(key)
    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print(111111111)
            login(request, user)
            context["message"] = "Successfully logged in"
            return render(request, 'djangoapp/general.html', context)
            
        else:
            print(2222222)
            form = AuthenticationForm()
            context['form']=form
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        print(33333333)
        return render(request, 'djangoapp/general.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    context = {}
    context["message"] = "Successfully logged out"
    return render(request, 'djangoapp/general.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    print("request", request)
    for key in request:
        print("key", key)
    context = {}
    if request.method == 'GET':
        print("BBBBBBBB")
        form = UserCreationForm()
        context['form']=form
        return render(request, 'djangoapp/signup.html', context)
    elif request.method == 'POST':
        # Check if user exists
        print("AAAAAAAAA")
        print("request", request)
        username = request.POST['Username']
        password = request.POST['Password']
        
        for field in request.POST:
            print("FIELD", field)
        password2 = request.POST['Password confirmation']
        print("password2", password2)
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist and password2 == password:
            print(44444444)
            user = User.objects.create_user(username=username,
                                            password=password)
            login(request, user)
            context['message']="User created successfully"
            return render(request, 'djangoapp/general.html', context)
        elif not user_exist:
            context['message'] = "Passwords didn't match."
            form = UserCreationForm()
            context['form']=form
            return render(request, 'djangoapp/signup.html', context)

        else:
            print(555555555)
            context['message'] = "User already exists."
            form = UserCreationForm()
            context['form']=form
            return render(request, 'djangoapp/signup.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealerships_by_id(request):
    if request.method == "GET":
        dealerId = int(request.GET["dealerId"])
        url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_id(url, dealerId=dealerId)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealerships_by_state(request):
    if request.method == "GET":
        state = request.GET["state"]
        url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/dealership/byId"
        # Get dealers from the URL
        dealerships = get_dealers_by_state(url, state=state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, **kwargs):
    context = {}
    if request.method == "POST":
        print(request)
        for key in request:
            print(key)
        if request.POST["dealerId"]:
            dealerId = request.POST["dealerId"]
            url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/review/"
            # Get dealers from the URL
            reviews = get_reviews_from_cf(url, dealerId=dealerId, **kwargs)
            for review in reviews:
                print(review)
            context["reviews"] = reviews
            context["dealerId"] = dealerId

    elif request.method == "GET":
        if "dealerId" in request.GET:
            dealerId = request.GET["dealerId"]
            url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/review/"
            # Get dealers from the URL
            reviews = get_reviews_from_cf(url, dealerId=dealerId, **kwargs)
            for review in reviews:
                print(review)
            context["reviews"] = reviews
            context["dealerId"] = dealerId

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...


def add_review(request):
    context={}
    if request.method == "POST":
        doc = copy.deepcopy(request.POST)
        url = "https://2123c0db.eu-gb.apigw.appdomain.cloud/api/dealership/"
        dealerId = doc["dealerId"]
        doc["dealership"] = dealerId
        doc["id"]=int(random.random()*10000000)
        # doc["purchase_date"]=doc["date"]
        print(doc)
        post_review(doc)
        context["dealerId"] = dealerId
    return render(request, 'djangoapp/dealer_details.html', context)


