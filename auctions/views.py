from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, CommentOnListing


def index(request):
    listings = Listing.objects.filter(isListed=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings,
        "categories": categories
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

def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create-listing.html",{
        "categories": categories
        })
    else:
        name = request.POST["name"]
        description = request.POST["description"]
        img = request.POST["img"]
        price = request.POST["price"]
        category = Category.objects.get(tag=request.POST["category"])
        user = request.user

        listing = Listing(name=name, description=description, img=img, price=price, category=category, listedBy=user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    

def filter_category(request):
    if request.method == "GET":
        category = request.GET["category"]
        category = Category.objects.get(tag=category)
        listings = category.all_products.all()
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": listings,
            "categories": categories
        })
    
def listing_details(request, id):
    listing = Listing.objects.get(id=id)
    if request.user in listing.watchlist.all():
        is_in_watchlist = True
    else:
        is_in_watchlist = False
    return render(request, "auctions/listing-details.html",{
        "id": id,
        "listing": listing,
        "is_in_watchlist": is_in_watchlist
    })

def remove_watchlist(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing-details", args=(id, )))

def add_watchlist(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing-details", args=(id, )))

def display_watchlist(request):
    user = request.user
    listings = user.user_watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

def add_comment(request, id):
    if request.method == "POST":
        user = request.user
        target_listing = Listing.objects.get(id=id)
        new_comment = request.POST["comment"]
        
        commentObj = CommentOnListing(author= user,listing = target_listing, comment = new_comment )
        commentObj.save()

        return HttpResponseRedirect(reverse("listing-details", args=(id, )))
