import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import User,Activity,Like

# Create your views here.

def index(request):
    activities = Activity.objects.all().order_by('-timestamp')

    for activity in activities:
        activity.likes = activity.likers.all()
        activity.logged_user_likes_post = activity.likes.filter(user=request.user).exists()
        activity.location_name = dict(Activity.LOCATIONS)[activity.location]
        activity.game_mode_name = dict(Activity.GAME_MODES)[activity.game_mode]
    paginator = Paginator(activities, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "scout/index.html", {
        "activities": page_obj
    })

def category(request,category):
    if any(key == category for key, value in Activity.AGE_RANGES):
        activities = Activity.objects.filter(age_range=category).order_by('-timestamp')

        paginator = Paginator(activities, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "scout/category.html", {
            "category": category,
            "activities": page_obj
        })
    else:
        raise Http404(f"{category} is not a valid input")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "scout/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "scout/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "scout/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "scout/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "scout/register.html")
    
# API route for search activities while typing
@csrf_exempt
def activities(request):

    activities = Activity.objects.all()

    search_options = []

    for activity in activities:
        search_options.append({'id':activity.id, 'title':activity.title})

    return JsonResponse({
        "message": "Activities retrieved successfully.",
        "result": search_options
        }, status=200)
