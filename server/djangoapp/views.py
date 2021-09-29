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
from .models import Certificate, Comment
from datetime import date

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def general(request):
    context = {"title": "Overview"}
 

    return render(request, 'djangoapp/general.html', context)

def resumee(request):
    context = {"title": "My Resumee",
               'image': 'photoCV haute resolution_cropped.png'}
 
    return render(request, 'djangoapp/resumee.html', context)

def comments(request):
    context = {"title": "Comments",
               'image': 'chat.png',
               'comments': []}
 

    if request.user.is_authenticated:
        author = request.user.username
    else:
        author = "Anonymous"

    context["author"] = author

    if request.method == "POST":
        posted_comment_text = request.POST["text"]
        date_today = date.today()
        comment = {
            "text": posted_comment_text,
            "author": author,
            "date": date,
        }
        comment = Comment(author=author, text=posted_comment_text)
        comment.save()

         # Retrieve Previous Comments
    comments = Comment.objects.all()
    for i, comment in enumerate(comments):
        comment_json = {
            "author": comment.author,
            "text": comment.text,
            "date": comment.date,
            "author_is_user": comment.author == request.user.username,
            "id": comment.id,
            # "img": comment.author.image,
        }
        context['comments'].append(comment_json)
    # print(context)

    return render(request, 'djangoapp/comments.html', context)

def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST['id']
        comment = Comment.objects.filter(id=comment_id)
        comment.delete()

    context = {"title": "Comments",
               'image': 'chat.png',
               'comments': []}
 
    comments = Comment.objects.all()
    for i, comment in enumerate(comments):
        comment_json = {
            "author": comment.author,
            "text": comment.text,
            "date": comment.date,
            "author_is_user": comment.author == request.user.username,
            "id": comment.id,
            # "img": comment.author.image,
        }
        context['comments'].append(comment_json)
    # print(context)

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
                "duration": certif.duration,
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
                    "duration": certif.duration
                }
                context["certifs"].append(certificate_json)
                context["skills"] = 1 # To have context["skills"] evaluated to True in order to have  an automatic scroll
        else:
            flags = []
            for flag in request.POST:
                flags.append(flag)
            context["flags"]=flags[1:]

            certifs = 0

            for flag in flags[1:]:
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
                    "duration": certif.duration
                }
                context["certifs"].append(certificate_json)

    return render(request, 'djangoapp/certificates.html', context)

def gallery(request):
    context = {"title": "Gallery",
               "image": "Art.jpg"}
 
    return render(request, 'djangoapp/gallery.html', context)

def fibromyalgia(request):
    context = {"title": "My Story",
               }
 
    return render(request, 'djangoapp/fibromyalgia.html', context)




# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {"title":"Log-in"}
 
    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            context['title'] = 'Comments'
            context['image'] = "chat.png"
            context['comments'] = []

            comments = Comment.objects.all()
            for i, comment in enumerate(comments):
                comment_json = {
                    "author": comment.author,
                    "text": comment.text,
                    "date": comment.date,
                    "author_is_user": comment.author == request.user.username,
                    "id": comment.id,
                    # "img": comment.author.image,
                }
                context['comments'].append(comment_json)

            return render(request, 'djangoapp/comments.html', context)
            
        else:
            form = AuthenticationForm()
            context['form']=form
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/general.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    context = {}
 

    context["message"] = "Successfully logged out"
    return render(request, 'djangoapp/general.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {"title":"SignUp"}

    if request.method == 'GET':
        form = UserCreationForm()
        context['form']=form
        return render(request, 'djangoapp/signup.html', context)
    elif request.method == 'POST':
        if "language" in request.POST.keys():
            context["language"] = request.POST["language"]
        else:
            context["language"] = "english"
        # Check if user exists
        username = request.POST['Username']
        password = request.POST['Password']
        password2 = request.POST['Password confirmation']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist and password2 == password:
            if len(password) < 8:
                context['message'] = "Your password must contain at least 8 characters."
                form = UserCreationForm()
                context['form']=form
                return render(request, 'djangoapp/signup.html', context)

            elif password == username:
                context['message'] = "Your password can’t be too similar to your other personal information."
                form = UserCreationForm()
                context['form']=form
                return render(request, 'djangoapp/signup.html', context)

            elif password in ['00000000', '12345678']:
                context['message'] = "Your password can’t be a commonly used password."
                form = UserCreationForm()
                context['form']=form
                return render(request, 'djangoapp/signup.html', context)

            try:
                int(password)
                context['message'] = "Your password can’t be entirely numeric."
                form = UserCreationForm()
                context['form']=form
                return render(request, 'djangoapp/signup.html', context)
            except:
                pass


            user = User.objects.create_user(username=username,
                                            password=password)
            login(request, user)
            context['title'] = 'Comments'
            context['image'] = "chat.png"
            context['comments'] = []

            comments = Comment.objects.all()
            for i, comment in enumerate(comments):
                comment_json = {
                    "author": comment.author,
                    "text": comment.text,
                    "date": comment.date,
                    "author_is_user": comment.author == request.user.username,
                    "id": comment.id,
                    # "img": comment.author.image,
                }
                context['comments'].append(comment_json)

            return render(request, 'djangoapp/comments.html', context)
        elif not user_exist:
            context['message'] = "Passwords didn't match."
            form = UserCreationForm()
            context['form']=form
            return render(request, 'djangoapp/signup.html', context)

        else:
            context['message'] = "User already exists."
            form = UserCreationForm()
            context['form']=form
            return render(request, 'djangoapp/signup.html', context)


# FRENCH VERSION

def generalFR(request):
    context = {"title": "Accueil"}
 

    return render(request, 'djangoapp/FR/general.html', context)

def resumeeFR(request):
    context = {"title": "Mon Curriculum Vitae",
               'image': 'photoCV haute resolution_cropped.png'}
 
    return render(request, 'djangoapp/FR/resumee.html', context)

def commentsFR(request):
    context = {"title": "Commentaires",
               'image': 'chat.png',
               'comments': []}
 

    if request.user.is_authenticated:
        author = request.user.username
    else:
        author = "Anonymous"

    context["author"] = author

    if request.method == "POST":
        posted_comment_text = request.POST["text"]
        date_today = date.today()
        comment = {
            "text": posted_comment_text,
            "author": author,
            "date": date,
        }
        comment = Comment(author=author, text=posted_comment_text)
        comment.save()

         # Retrieve Previous Comments
    comments = Comment.objects.all()
    for i, comment in enumerate(comments):
        comment_json = {
            "author": comment.author,
            "text": comment.text,
            "date": comment.date,
            "author_is_user": comment.author == request.user.username,
            "id": comment.id,
            # "img": comment.author.image,
        }
        context['comments'].append(comment_json)
    # print(context)

    return render(request, 'djangoapp/FR/comments.html', context)

def delete_commentFR(request):
    if request.method == "POST":
        comment_id = request.POST['id']
        comment = Comment.objects.filter(id=comment_id)
        comment.delete()

    context = {"title": "Commentaires",
               'image': 'chat.png',
               'comments': []}
 
    comments = Comment.objects.all()
    for i, comment in enumerate(comments):
        comment_json = {
            "author": comment.author,
            "text": comment.text,
            "date": comment.date,
            "author_is_user": comment.author == request.user.username,
            "id": comment.id,
            # "img": comment.author.image,
        }
        context['comments'].append(comment_json)
    # print(context)

    return render(request, 'djangoapp/FR/comments.html', context)

def certificatesFR(request):

    context = {"title": "Mes Certificats et Diplômes",
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
                "duration": certif.duration,
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
                    "duration": certif.duration
                }
                context["certifs"].append(certificate_json)
                context["skills"] = 1 # To have context["skills"] evaluated to True in order to have  an automatic scroll
        else:
            flags = []
            for flag in request.POST:
                flags.append(flag)
            context["flags"]=flags[1:]

            certifs = 0

            for flag in flags[1:]:
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
                    "duration": certif.duration
                }
                context["certifs"].append(certificate_json)

    return render(request, 'djangoapp/FR/certificates.html', context)

def galleryFR(request):
    context = {"title": "Gallerie",
               "image": "Art.jpg"}
 
    return render(request, 'djangoapp/FR/gallery.html', context)

def fibromyalgiaFR(request):
    context = {"title": "Mon Histoire",
               }
 
    return render(request, 'djangoapp/FR/fibromyalgia.html', context)




# Create a `login_request` view to handle sign in request
def login_requestFR(request):
    context = {"title":"Log-in"}
 
    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            context['title'] = 'Comments'
            context['image'] = "chat.png"
            context['comments'] = []

            comments = Comment.objects.all()
            for i, comment in enumerate(comments):
                comment_json = {
                    "author": comment.author,
                    "text": comment.text,
                    "date": comment.date,
                    "author_is_user": comment.author == request.user.username,
                    "id": comment.id,
                    # "img": comment.author.image,
                }
                context['comments'].append(comment_json)

            return render(request, 'djangoapp/FR/comments.html', context)

        else:
            form = AuthenticationForm()
            context['form']=form
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/FR/login.html', context)
    else:
        return render(request, 'djangoapp/FR/general.html', context)


# Create a `logout_request` view to handle sign out request
def logout_requestFR(request):
    logout(request)
    context = {}
 

    context["message"] = "Vous êtes bien déconnecté"
    return render(request, 'djangoapp/FR/general.html', context)

# Create a `registration_request` view to handle sign up request
def registration_requestFR(request):
    context = {"title":"S'inscrire"}

    if request.method == 'GET':
        

        form = UserCreationForm()
        context['form']=form
        return render(request, 'djangoapp/FR/signup.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['Username']
        password = request.POST['Password']
        password2 = request.POST['Password confirmation']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist and password2 == password:
            if len(password) < 8:
                context['message'] = "Votre mot de passe doit contenir au moins 8 caractères."
                form = UserCreationForm()
                context['form'] = form
                return render(request, 'djangoapp/FR/signup.html', context)

            elif password == username:
                context['message'] = "Votre mot de passe ne peut pas être identique à votre nom d'utilisateur."
                form = UserCreationForm()
                context['form']=form
                return render(request, 'djangoapp/FR/signup.html', context)

            elif password in ['00000000', '12345678']:
                context['message'] = "Votre mot de passe ne doit pas être trop commun."
                form = UserCreationForm()
                context['form']=form
                return render(request, 'djangoapp/FR/signup.html', context)

            try:
                int(password)
                context['message'] = "Votre mot de passe ne peut pas être entièrement numérique."
                form = UserCreationForm()
                context['form']=form
                return render(request, 'djangoapp/FR/signup.html', context)
            except:
                pass


            user = User.objects.create_user(username=username,
                                            password=password)
            login(request, user)
            context['title'] = 'Comments'
            context['image'] = "chat.png"
            context['comments'] = []

            comments = Comment.objects.all()
            for i, comment in enumerate(comments):
                comment_json = {
                    "author": comment.author,
                    "text": comment.text,
                    "date": comment.date,
                    "author_is_user": comment.author == request.user.username,
                    "id": comment.id,
                    # "img": comment.author.image,
                }
                context['comments'].append(comment_json)

            return render(request, 'djangoapp/FR/comments.html', context)
        elif not user_exist:
            context['message'] = "Les mots de passe ne correspondent pas."
            form = UserCreationForm()
            context['form']=form
            return render(request, 'djangoapp/FR/signup.html', context)

        else:
            context['message'] = "Un utilisateur avec ce pseudo existe déjà."
            form = UserCreationForm()
            context['form']=form
            return render(request, 'djangoapp/FR/signup.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships

