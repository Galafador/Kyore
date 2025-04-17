from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models


class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    watchlist = models.ManyToManyField("Listing", related_name="watchlisted_by", blank=True)
    image_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.username}"
    def add_to_watchlist(self, listing):
        self.watchlist.add(listing)
    def remove_from_watchlist(self, listing):
        self.watchlist.remove(listing)
    def is_in_watchlist(self, listing):
        return self.watchlist.filter(id=listing.id).exists()

class Category(MPTTModel):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True, blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    class MPPTMeta:
        order_insertion_by = ['name']
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="listings", null=True)
    is_active = models.BooleanField(default=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="highest_bidder", null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="wins", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.title}"
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    is_first_bid = models.BooleanField(default=True)
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="bids", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Bid by {self.bidder}: ${self.amount} on '{self.listing.title}' at {self.created_at}"
    
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256, null=True)
    def __str__(self):
        return f"'{self.comment}' by {self.commenter} on '{self.listing.title}'"


