from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from .models import *


def index(request):
    active_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "active_listings" : active_listings
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


@login_required
def create(request): 
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST.get("category", "")
        starting_bid = float(request.POST["starting_bid"])
        image_url = request.POST.get("image_url", "")

        Listing.objects.create(title=title,
                            description=description,
                            category=category,
                            starting_bid=starting_bid,
                            image_url=image_url)
        
        return HttpResponseRedirect(reverse("Index"))

    categories = Category.objects.all() + []
    return render(request, "auction/create.html", {
        "listing" : Listing,
        "categories" : categories,
    })

def categories_view(request):
    root_categories = Category.objects.filter(parent__isnull=True)

    return render(request, "auctions/categories.html",{
        "root_categories" : root_categories
    })

#a view to handle ajax request to fetch child categories.
def get_child_categories(request):
    parent_id = request.GET.get("parent_id")
    if not parent_id:
        return JsonResponse({"error": "No parent_id provided"}, status=400)
    try:
        parent_category = Category.objects.get(id=parent_id)
        child_categories = parent_category.get_children()
        data = [{"id": cat.id, "name": cat.name, "is_leaf":cat.is_leaf_node()} for cat in child_categories]
        return JsonResponse({"child_categories" : data})
    except Category.DoesNotExist:
        return JsonResponse({"error": "Parent category not found."}, status=404)


def listing(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, "auctions/listing.html", {
        "title" : listing.title,
        "description" : listing.description,
        "image_url" : listing.image_url,
        "starting_bid": listing.starting_bid,
        "highest_bid": listing.highest_bid,
        "highest_bidder": listing.highest_bidder
    })