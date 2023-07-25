from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, CommentOnListing, Bid


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
    user = request.user
    listing = Listing.objects.get(id=id)
    is_sold = listing.is_closed
    close = False
    if user == listing.listedBy:
        close = True
    comments = listing.listing_comments.all()
    placed_bid = listing.placed_bid
    if request.user in listing.watchlist.all():
        is_in_watchlist = True
    else:
        is_in_watchlist = False
    return render(request, "auctions/listing-details.html",{
        "id": id,
        "listing": listing,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
        "placed_bid": placed_bid,
        "close": close,
        "is_sold": is_sold
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
    
def place_bid(request, id):
     if request.method == "POST":
        target_user = request.user
        target_listing = Listing.objects.get(id=id)
        new_bid_price = float(request.POST["bid_price"])
        placed_bid = target_listing.placed_bid
        new_bid = Bid(user = target_user, bid_price = new_bid_price)
        new_bid.save()
        if placed_bid == None:
            if new_bid_price >= target_listing.price:
                target_listing.placed_bid = new_bid
                target_listing.save()
                return HttpResponseRedirect(reverse("listing-details", args=(id, )))
            else:
                return HttpResponseRedirect(reverse("error", args=("initial-price", )))
        elif placed_bid.bid_price < new_bid_price:
            target_listing.placed_bid = new_bid
            target_listing.save()
            return HttpResponseRedirect(reverse("listing-details", args=(id, )))
        else:
            return HttpResponseRedirect(reverse("error", args=("bid-price", )))


def close(request, id):
    target_listing = Listing.objects.get(id=id)
    target_listing.is_closed = True
    target_listing.save()
    return HttpResponseRedirect(reverse("listing-details", args=(id, )))

def error(request, err):
    return render(request, "auctions/bid-error.html",{
            "err": err,
        })