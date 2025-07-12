from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment, Favorite
from .forms import ListingForm


def get_child_categories(request):
    parent_id = request.GET.get("parent_id")
    if not parent_id:
        return JsonResponse({"error": "No parent_id provided"}, status=400)
    try:
        parent_category = Category.objects.get(pk=parent_id)
        child_categories = parent_category.children.all()
        data = [{"id": cat.id, "name": cat.name, "parentId": parent_id, "has_children": cat.has_children()} for cat in child_categories]
        return JsonResponse({"child_categories": data}, status=200)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Parent category not found."}, status=404)

def get_category_breadcrumb(request):
    category_id = request.GET.get('category_id')
    if not category_id:
        return JsonResponse({"breadcrumb": []})
    try:
        category = Category.objects.get(pk=category_id)
        breadcrumb = []
        while category:
            breadcrumb.insert(0, {"id": category.id, "name": category.name})
            category = category.parent
        return JsonResponse({"breadcrumb": breadcrumb})
    except Category.DoesNotExist:
        print('category does not exist')
        return JsonResponse({"breadcrumb": []})


def get_favorited_listing_ids(request):
    if request.user.is_authenticated:
        favorited_listing_ids = set(Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True))
    else:
        favorited_listing_ids = set()
    return favorited_listing_ids

def index(request):
    # Initialize contexts before rendering
    active_listings = Listing.objects.filter(is_active=True)
    favorited_listing_ids = get_favorited_listing_ids(request)

    #TODO: create a function/algorithm to determine the top categories and pass to template. currently hardcoded.

    return render(request, "auctions/index.html", {
        "active_listings" : active_listings,
        "favorited_listing_ids": favorited_listing_ids
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
            #redirect to 'next' in query parameter if exists, else go to index
            next_url = request.POST.get('next') or reverse("index")
            return HttpResponseRedirect(next_url)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        next_url = request.GET.get("next", "")
        return render(request, "auctions/login.html", {
            "next": next_url
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        if not username:
            return render(request, "auctions/register.html", {
                "message": "Invalid username."
            })
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
def create_listing(request):
    root_categories = Category.objects.filter(parent__isnull=True)

    if request.method == "POST":
        form = ListingForm(request.POST)
        
        #manually attach the category before validating the form
        category_id = request.POST.get("category")
        print(f'category Id is {category_id}')
        
        if not category_id:
            print('Category is NOT provided')
            form.add_error('category', "Please input category.")
        else:
            try:
                category_instance = Category.objects.get(pk=category_id)
                form.instance.category = category_instance
                print(f'form.instance.category is {form.instance.category}')
            except Category.DoesNotExist:
                form.add_error('category', "Selected category does not exist.")

        if form.is_valid():
            try:
                print('form is valid')
                new_listing = form.save(commit=False)
                print(new_listing)
                new_listing.seller = request.user
                new_listing.save()
                messages.success(request, "Listing added successfully!")
                return HttpResponseRedirect(reverse("listing", args=[new_listing.id]))
            except(ValueError, TypeError):
                messages.error(request, "Something went wrong when saving. Please try again.")
        else:
            print('form is NOT valid')
            form.add_is_invalid_class()
            messages.error(request, "Please correct the errors below.")

    else:
        form = ListingForm()

    return render(request, "auctions/create.html", {
        "form": form,
        "root_categories": root_categories
    })

def categories(request):
    category_id = request.GET.get('categoryId')
    
    # Initialize contexts for template
    favorited_listing_ids = get_favorited_listing_ids(request)
    root_categories= Category.objects.filter(parent__isnull=True)

    #initialize listings and category
    listings = []
    category = []

    if not category_id: #GET with empty query parameter
        return render(request, "auctions/categories.html", {
        "root_categories": root_categories
        })
    
    try:
        category = Category.objects.get(id=int(category_id))
        descendant_category_ids = category.get_descendants_ids()
        listings = Listing.objects.filter(category_id__in=descendant_category_ids)
        if not listings.exists():
            messages.error(request, "No listings found in this category")
    except (UnboundLocalError, Category.DoesNotExist, ValueError, TypeError):
        messages.error(request, "Invalid category selected.")
    return render(request, "auctions/categories.html", {
        "root_categories": root_categories,
        "listings": listings,
        "category": category,
        "favorited_listing_ids": favorited_listing_ids
    })

def listing(request, id):
    listing = Listing.objects.get(id=id)
    favorited_listing_ids = get_favorited_listing_ids(request)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "favorited_listing_ids": favorited_listing_ids
    })

@login_required
def watchlist_view(request):
    favorited_listing_ids = get_favorited_listing_ids(request)
    watchlist = Listing.objects.filter(favorites__user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "favorited_listing_ids": favorited_listing_ids
    })

# A view to handle ajax request to toggle favorited status of a listing
@login_required
def favorite_listing(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
        if not created:
            #already favorited, will remove from favorite
            favorite.delete()
            favorited = False
            message = "Removed from watchlist."
        else:
            favorited = True
            message = "Added to watchlist."

        favorites_count = Favorite.objects.filter(listing=listing).count()

        return JsonResponse({
            "favorited": favorited,
            "favorites_count": favorites_count,
            "message": message
        })
    return JsonResponse({"error": "Invalid response. GET instead of POST."}, status=400)