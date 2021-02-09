from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category

def getName(category):
    return (category.name, category.name)

class NewListingForm(forms.Form):
    title = forms.CharField(label="Listing Title")
    description = forms.CharField(label="Description")
    bid = forms.FloatField(label="Starting Bid", min_value=0.01)
    imageURL = forms.URLField(label="Image URL")
    category = forms.CharField(label="Category", widget=forms.Select(choices=map(getName, Category.objects.all())))

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def addListing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            category = Category.objects.all().filter(name=form.cleaned_data['category']).get()
            bid = Bid(user = user, price=bid)
            bid.save()
            imageURL = form.cleaned_data['imageURL']
            listing = Listing(user=user, title=title, description=description, bid=bid, imgURL=imageURL)
            listing.save()
            category.listing.add(listing)
            category.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/addListing.html", {
                "form": form
            })
    return render(request, "auctions/addListing.html", {
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

def watchlist(request):
    listings = Listing.objects.all()
    def containsUser(listing):
        if request.user in listing.watchList:
            return True
        else:
            return False
    watchList = filter(containsUser, listings)
    return render(request, "auctions/watchList.html", {
        "watchlist": watchList
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category_id):
    return render(request, "auctions/category.html", {
        "category": Category.objects.get(pk=category_id)
    })

def listing(request, listing_id):
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id)
    })