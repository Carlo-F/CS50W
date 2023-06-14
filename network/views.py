import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User,Post,Follow,Like


def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    for post in posts:
        post.likes = post.likers.all()
        post.logged_user_likes_post = post.likes.filter(user=request.user).exists()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })

@login_required
def following(request):

    follows = request.user.following.all()

    posts = Post.objects.filter(user__id__in=follows.values_list('following_user_id')).order_by('-timestamp')

    for post in posts:
        post.likes = post.likers.all()
        post.logged_user_likes_post = post.likes.filter(user=request.user).exists()


    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

@login_required
def profile(request,username):
    try:
        profile_user = User.objects.get(username=username)
        posts = Post.objects.filter(user=profile_user).order_by('-timestamp')

        for post in posts:
            post.likes = post.likers.all()
            post.logged_user_likes_post = post.likes.filter(user=request.user).exists()

        followers = profile_user.followers.all()
        follows = profile_user.following.all()
        profile_user.logged_user_is_following = profile_user.followers.filter(user=request.user)

        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/profile.html", {
                "profile_user": profile_user,
                "page_obj":page_obj,
                "followers":followers,
                "follows":follows
            })
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"User with id {username} does not exist."
        }, status=400)

@csrf_exempt
@login_required
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    user_id = data.get('user_id')

    if len(user_id) == 0:
        return JsonResponse({"error": "user_id is required"}, status=400)
    elif(user_id == request.user.id):
        return JsonResponse({"error": "You cannot follow yourself!"}, status=400)
    
    Follow.objects.create(user_id=request.user.id, following_user_id=user_id)
    
    return JsonResponse({"message": "Success"}, status=201)

@csrf_exempt
@login_required
def unfollow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    user_id = data.get('user_id')

    if len(user_id) == 0:
        return JsonResponse({"error": "user_id is required"}, status=400)
    
    Follow.objects.filter(user_id=request.user.id, following_user_id=user_id).delete()
    
    return JsonResponse({"message": "Success"}, status=201)

@csrf_exempt
@login_required
def like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    post_id = data.get('post_id')

    if len(post_id) == 0:
        return JsonResponse({"error": "post_id is required"}, status=400)
    
    Like.objects.create(user_id=request.user.id, liked_post_id=post_id)
    
    return JsonResponse({"message": "Success"}, status=201)

@csrf_exempt
@login_required
def dislike(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    post_id = data.get('post_id')

    if len(post_id) == 0:
        return JsonResponse({"error": "post_id is required"}, status=400)
    
    Like.objects.filter(user_id=request.user.id, liked_post_id=post_id).delete()
    
    return JsonResponse({"message": "Success"}, status=201)

@csrf_exempt
@login_required
def edit_post(request,post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    if len(data.get('content')) == 0:
        return JsonResponse({"error": "post content is required"}, status=400)
    
    Post.objects.filter(id=post_id,user=request.user).update(content=data.get('content'))

    return JsonResponse({"message": "Post saved successfully."}, status=201)

@csrf_exempt
@login_required
def new_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    if len(data.get('content')) == 0:
        return JsonResponse({"error": "post content is required"}, status=400)

    new_post = Post(
        content=data.get('content'),
        user=request.user
    )

    new_post.save()

    return JsonResponse({"message": "New Post saved successfully."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
