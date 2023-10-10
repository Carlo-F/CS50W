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
from django import forms

from .models import User,Activity,Like,EducationalGoal
from .utils import get_formatted_activities

class NewActivityForm(forms.Form):

    activity_title = forms.CharField(label="title",widget=forms.TextInput(attrs={"class": "form-control mb-4"}))
    activity_age_range = forms.ChoiceField(choices=Activity.AGE_RANGES,label="age range", widget=forms.Select(attrs={"class":"form-control mb-4"}))
    activity_location = forms.ChoiceField(choices=Activity.LOCATIONS,label="location", widget=forms.Select(attrs={"class":"form-control mb-4"}))
    activity_educational_goals = forms.ChoiceField(choices=EducationalGoal.EDUCATIONAL_GOALS,label="educational goal", widget=forms.Select(attrs={"class":"form-control mb-4"}))
    activity_duration = forms.IntegerField(min_value=1, required=True, label="duration (in minutes)",widget=forms.NumberInput(attrs={"class": "form-control mb-4"}))
    activity_required_materials = forms.CharField(label="required materials", required=False, widget=forms.TextInput(attrs={"class": "form-control mb-4"}))
    activity_method = forms.CharField(widget=forms.Textarea(attrs={"rows":"5", "class": "form-control mb-4"}))
    activity_game_mode = forms.ChoiceField(choices=Activity.GAME_MODES,label="game mode", widget=forms.Select(attrs={"class":"form-control mb-4"}))
    activity_is_suitable_for_disabled = forms.BooleanField(label="Is suitable for disabled?", required=False, widget=forms.CheckboxInput(attrs={"class":"mb-4"}))

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
    likes = Like.objects.all().order_by('-timestamp')
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

    likes = Like.objects.filter(user=request.user).order_by('-timestamp')
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

@login_required
def new_activity(request):

    if request.method == "POST":
        form = NewActivityForm(request.POST)

        if form.is_valid():
            activity_title = form.cleaned_data['activity_title']
            activity_age_range = form.cleaned_data['activity_age_range']
            activity_location = form.cleaned_data['activity_location']
            activity_educational_goals = form.cleaned_data['activity_educational_goals']
            activity_duration = form.cleaned_data['activity_duration']
            activity_required_materials = form.cleaned_data['activity_required_materials']
            activity_method = form.cleaned_data['activity_method']
            activity_game_mode = form.cleaned_data['activity_game_mode']
            activity_is_suitable_for_disabled = form.cleaned_data['activity_is_suitable_for_disabled']

            new_activity = Activity(
                title=activity_title,
                user=request.user,
                age_range=activity_age_range,
                location=activity_location,
                educational_goals=activity_educational_goals,
                duration=activity_duration,
                required_materials=activity_required_materials,
                method=activity_method,
                game_mode=activity_game_mode,
                is_suitable_for_disabled=activity_is_suitable_for_disabled
            )

            new_activity.save()

            return HttpResponseRedirect(reverse("my_activities"))
    else:
        return render(request, "scout/new_activity.html",{
            "form": NewActivityForm(),
            "current_page": "new_activity"
        })
    
@login_required
def delete_activity(request,activity_id):
    activity = Activity.objects.get(id=activity_id)

    if activity.user != request.user:
        return HttpResponseRedirect(reverse("index"))

    activity.delete()

    return HttpResponseRedirect(reverse("my_activities"))

@login_required
def edit_activity(request,activity_id):
    activity = Activity.objects.get(id=activity_id, user=request.user)

    if request.method == "POST":
        form = NewActivityForm(request.POST)

        if form.is_valid():

            activity.title = form.cleaned_data['activity_title']
            activity.age_range = form.cleaned_data['activity_age_range']
            activity.location = form.cleaned_data['activity_location']
            activity.educational_goals = form.cleaned_data['activity_educational_goals']
            activity.duration = form.cleaned_data['activity_duration']
            activity.required_materials = form.cleaned_data['activity_required_materials']
            activity.method = form.cleaned_data['activity_method']
            activity.game_mode = form.cleaned_data['activity_game_mode']
            activity.is_suitable_for_disabled = form.cleaned_data['activity_is_suitable_for_disabled']

            activity.save()

            return HttpResponseRedirect(reverse("activity",kwargs={'activity_id':activity.id}))
    else:

        form = NewActivityForm(initial={
            'activity_title': activity.title,
            'activity_age_range': activity.age_range,
            'activity_location': activity.location,
            'activity_educational_goals': activity.educational_goals,
            'activity_duration': activity.duration,
            'activity_required_materials': activity.required_materials,
            'activity_method': activity.method,
            'activity_game_mode': activity.game_mode,
            'activity_is_suitable_for_disabled': activity.is_suitable_for_disabled
        })

        return render(request, "scout/edit_activity.html",{
            "form": form,
            "current_page": "my_activities",
            "activity": activity
        })


@login_required
def my_activities(request):

    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')

    formatted_activities = get_formatted_activities(request.user,activities)

    paginator = Paginator(formatted_activities, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "scout/my_activities.html", {
        "my_activities": page_obj,
        "current_page": "my_activities"
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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("my_activities"))
        else:
            return render(request, "scout/login.html", {
                "message": "Invalid username and/or password.",
                "current_page": "login"
            })
    else:
        return render(request, "scout/login.html",{
        "current_page": "login"
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username= request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "scout/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "scout/register.html", {
                "message": "username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("my_activities"))
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