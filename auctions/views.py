from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User,Listing

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
        #current price by default is equal to the starting_bid
        listing.price = listing.starting_bid

        #if there are any bids on the listing, current price is equal to the higher bid
        bids = listing.bids.order_by('-amount')
        if bids:
            listing.price = listing.bids.order_by('-amount')[0].amount

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
