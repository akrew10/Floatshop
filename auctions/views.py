from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Wear, Category, Listing, Comment, bid


def index(request):
    listings = Listing.objects.filter(Active = True)
    guns = Category.objects.all()
    return render(request, "auctions/index.html",{
            "listings" : listings,
            "guns": guns
            })

def category(request):
    if request.method =="POST":
        CategoryFrom = request.POST['category']
     
        category = Category.objects.get(categoryName = CategoryFrom)
        listings = Listing.objects.filter(Active = True, category=category)
        guns = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings" : listings,
            "guns": guns,
            "categoryf": CategoryFrom
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
    if request.method == "POST":

        title = request.POST["title"]
        photo = request.POST["photo"]
        startprice = request.POST["startprice"]
        buyprice = request.POST["buyoutprice"]
        wear = request.POST["wear"]
        Float = request.POST["float"]
        gun = request.POST["gun"]
        if "StatTrak" in request.POST["stattrak"]:
            Statrak = True
        else:
            Statrak = False
        currentuser = request.user

        gunData = Category.objects.get(categoryName = gun)
        wearData = Wear.objects.get(WearName = wear)
        
        buyprice = float(buyprice)

        bidprices = bid(bidprice=int(startprice), user=currentuser)
        bidprices.save()
        


        listing = Listing(
            title = title,
            photo = photo,
            startprice = bidprices,
            buyprice = buyprice,
            wear = wearData,
            float = float(Float),
            category = gunData,
            owner = currentuser,
            StatTrak = Statrak

        )
        listing.save()
        return HttpResponseRedirect(reverse(index))
    else:
        wears = Wear.objects.all()
        guns = Category.objects.all()
        return render(request, "auctions/createlisting.html",{
        "wears": wears,
        "guns" : guns
        })
    
def listing(request, Listing_id):
    listings = Listing.objects.get(pk=Listing_id)
    isWatch = request.user in listings.watchlist.all()
    currentuser = request.user
    comments = Comment.objects.filter(comments = listings)
    isOwner = request.user.username == listings.owner.username
    return render(request,"auctions/listing.html",{
        "listing": listings,
        "isWatch": isWatch,
        "currentuser" : currentuser,
        "comments" : comments,
        "isOwner" : isOwner
    })

def addComment(request, Listing_id):
    listingData = Listing.objects.get(pk=Listing_id)
    currentUser = request.user
    comment = request.POST["comment"]
    newComment = Comment(
        author = currentUser,
        comment = comment,
        comments = listingData
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(Listing_id, )))

def addBid(request, Listing_id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=Listing_id)
    isOwner = request.user.username == listingData.owner.username
    isWatch = request.user in listingData.watchlist.all()
    comments = Comment.objects.filter(comments = listingData)
    if int(newBid) > listingData.startprice.bidprice:
        updateBid = bid(user=request.user, bidprice=int(newBid))
        updateBid.save()
        listingData.startprice = updateBid
        listingData.save()
       
        return render(request, "auctions/listing.html", {
            "message": "Successful Bid!",
            "listing": listingData,
            "update": True,
            "allComments": comments,
            "isOwner" : isOwner,
             "isWatch":isWatch
        }) 
    else:
         return render(request, "auctions/listing.html", {
            "message": "Failed Bid.",
            "listing": listingData,
            "update": False,
            "allComments": comments,
            "isOwner" : isOwner,
             "isWatch":isWatch
        }) 
    



def removeWatchlist(request, Listing_id):
    listingData = Listing.objects.get(pk=Listing_id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(Listing_id, )))


def addWatchlist(request, Listing_id):
    listingData = Listing.objects.get(pk=Listing_id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(Listing_id, )))


def watchlist(request):
    currentUser = request.user
    listings = currentUser.watchinglist.all()
    guns = Category.objects.all()
    return render(request, "auctions/watchlist.html",{
            "listings" : listings,
            "guns": guns
            })

def closeAuction(request, Listing_id):
   listingData = Listing.objects.get(pk=Listing_id)
   listingData.Active = False
   listingData.save()
   comments = Comment.objects.filter(comments = listingData)
   isOwner = request.user.username == listingData.owner.username
   return render(request, "auctions/listing.html", {
            "message": "Successful Bid!",
            "listing": listingData,
            "update": True,
            "allComments": comments,
            "isOwner" : isOwner,
            "message": "Auction Closed"
        }) 