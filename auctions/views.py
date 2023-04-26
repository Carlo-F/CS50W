from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms

from .models import User,Listing,Watchlist
from .utils import get_listing_price

class NewListingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    listing_title = forms.CharField(label="title")
    listing_description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    listing_starting_bid = forms.IntegerField(min_value=1, required=True, label="starting bid")
    listing_image_url = forms.CharField(label="image url")
    listing_category = forms.CharField(label="category")


def index(request):
    active_listings = Listing.objects.filter(is_active=True)

    for listing in active_listings:
        #get highest bid or starting_bid
        listing.price = get_listing_price(listing)

    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

@login_required
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)

        if form.is_valid():
            listing_title = form.cleaned_data['listing_title']
            listing_description = form.cleaned_data['listing_description']
            listing_starting_bid = form.cleaned_data['listing_starting_bid']
            listing_image_url = form.cleaned_data['listing_image_url']
            listing_category = form.cleaned_data['listing_category']

            new_listing = Listing(
                title=listing_title,
                description=listing_description,
                starting_bid=listing_starting_bid,
                image_url=listing_image_url,
                category=listing_category,
                owner=request.user
            )

            new_listing.save()

            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html",{
            "form": NewListingForm()
        })

@login_required
def watch(request, listing_id):
    #watch the listing
    listing = Listing.objects.get(pk=listing_id)

    watchlist = Watchlist.objects.get_or_create(owner=request.user)

    watchlist[0].listings.add(listing)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def unwatch(request, listing_id):
    #unwatch the listing
    listing = Listing.objects.get(pk=listing_id)

    watchlist = Watchlist.objects.get(owner=request.user)

    watchlist.listings.remove(listing)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user_watchlist = Watchlist.objects.get(owner=request.user)

    #get highest bid or starting_bid
    listing.price = get_listing_price(listing)
    winning_bid = None
    bids = listing.bids.order_by('-amount')
    if bids:
        winning_bid = bids[0]
    
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "winning_bid": winning_bid,
        "watchlist": user_watchlist,
    })

def categories(request):
    active_listings = Listing.objects.filter(is_active=True)
    categories = []

    for listing in active_listings:
        if listing.category is not None and not listing.category in categories:
            categories.append(listing.category)

    return render(request, "auctions/categories.html", {"categories": categories})

def category(request, category):
    active_listings = Listing.objects.filter(category=category)

    for listing in active_listings:
        #get highest bid or starting_bid
        listing.price = get_listing_price(listing)

    return render(request, "auctions/index.html", {
        "category": category,
        "active_listings": active_listings
    })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
