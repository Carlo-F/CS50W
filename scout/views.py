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
from .utils import get_formatted_activities

# Create your views here.

def index(request):
    activities = Activity.objects.all().order_by('-timestamp')[:3]

    formatted_activities = get_formatted_activities(request.user,activities)

    likes = Like.objects.all()[:3]
    popular_activities = []

    for like in likes:
        if like.liked_activity not in popular_activities:
            popular_activities.append(like.liked_activity)
    
    formatted_popular_activities = get_formatted_activities(request.user,popular_activities)

    return render(request, "scout/index.html", {
        "latest_activities": formatted_activities,
        "popular_activities": formatted_popular_activities,
        "current_page": "home"
    })

def activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        formatted_activity = get_formatted_activities(request.user,[activity])[0]
        similar_activities = Activity.objects.filter(age_range=activity.age_range, location=activity.location, game_mode=activity.game_mode).exclude(id=activity_id).order_by('-timestamp')[:3]

        formatted_similar_activities = get_formatted_activities(request.user,similar_activities)

        return render(request, "scout/activity.html", {
            "activity": formatted_activity,
            "current_page": "activity",
            "similar_activities": formatted_similar_activities
        })
        
    except Activity.DoesNotExist:
        raise Http404(f"Activity with id {activity_id} does not exist.")

def latest(request):
    activities = Activity.objects.all().order_by('-timestamp')

    formatted_activities = get_formatted_activities(request.user,activities)

    paginator = Paginator(formatted_activities, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "scout/latest.html", {
        "latest_activities": page_obj,
        "current_page": "latest"
    })

def popular(request):
    likes = Like.objects.all()
    activities = []

    for like in likes:
        if like.liked_activity not in activities:
            activities.append(like.liked_activity)

    formatted_activities = get_formatted_activities(request.user,activities)

    paginator = Paginator(formatted_activities, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "scout/popular.html", {
        "popular_activities": page_obj,
        "current_page": "popular"
    })

@login_required
def favourites(request):

    likes = Like.objects.filter(user=request.user)
    activities = []

    for like in likes:
        if like.liked_activity not in activities:
            activities.append(like.liked_activity)

    formatted_activities = get_formatted_activities(request.user,activities)

    paginator = Paginator(formatted_activities, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "scout/favourites.html", {
        "favourite_activities": page_obj,
        "current_page": "favourites"
    })

def tags(request):
    tags = Activity.LOCATIONS + Activity.GAME_MODES
    # additional tags
    tags.extend([("is_suitable_for_disabled", "Suitable for disabled")])

    return render(request, "scout/tags.html",{
        "tags": tags,
        "current_page": "tags"
    })

def tag(request,tag):
    activities = []
    if any(key == tag for key, value in Activity.LOCATIONS):
        activities = Activity.objects.filter(location=tag).order_by('-timestamp')
    elif any(key == tag for key, value in Activity.GAME_MODES):
        activities = Activity.objects.filter(game_mode=tag).order_by('-timestamp')
    elif tag == 'is_suitable_for_disabled':
        activities = Activity.objects.filter(is_suitable_for_disabled=1).order_by('-timestamp')

    formatted_activities = get_formatted_activities(request.user,activities)

    paginator = Paginator(formatted_activities, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "scout/tag.html",{
        "tag": tag,
        "activities": page_obj,
        "current_page": "tags"
    })

def category(request,category):
    if any(key == category for key, value in Activity.AGE_RANGES):
        activities = Activity.objects.filter(age_range=category).order_by('-timestamp')

        formatted_activities = get_formatted_activities(request.user,activities)

        paginator = Paginator(formatted_activities, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "scout/category.html", {
            "category": category,
            "activities": page_obj,
            "current_page": "category"
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
        return render(request, "scout/login.html",{
        "current_page": "login"
        })


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
        return render(request, "scout/register.html",{
        "current_page": "register"
        })
    
# API route for search activities by title while typing
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

@csrf_exempt
@login_required
def like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    activity_id = data.get('activity_id')

    if len(activity_id) == 0:
        return JsonResponse({"error": "activity_id is required"}, status=400)
    
    Like.objects.create(user_id=request.user.id, liked_activity_id=activity_id)
    
    return JsonResponse({"message": "Success"}, status=201)

@csrf_exempt
@login_required
def dislike(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    activity_id = data.get('activity_id')

    if len(activity_id) == 0:
        return JsonResponse({"error": "activity_id is required"}, status=400)
    
    Like.objects.filter(user_id=request.user.id, liked_activity_id=activity_id).delete()
    
    return JsonResponse({"message": "Success"}, status=201)