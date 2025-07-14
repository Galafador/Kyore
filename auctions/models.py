from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    watchlist = models.ManyToManyField("Listing", related_name="watchlisted_by", blank=True)
    image_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
            return f"{self.name}"
    def get_ancestors(self):
        """
        returns an array of all ancestors
        """
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors[::1] #return in order of oldest ancestor to immediate parent
    def get_descendants_ids(self):
        """
        returns an array of all descendants ids plus itself recursively
        """
        descendants_ids = [self.id]
        def getIds(children):
            for child in children:
                descendants_ids.append(child.id)
                getIds(child.children.all())
        getIds(self.children.all())
        return descendants_ids
    def has_children(self):
        return self.children.exists()


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="listings", null=True)
    is_active = models.BooleanField(default=True)
    starting_bid = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    highest_bid = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="highest_bidder", null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="wins", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(null=True, blank=True)
    has_bids = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        #checks if this is a new listing, for creation / update logic
        is_new = self.pk is None
        
        # Save first to get primary key if new
        super().save(*args, **kwargs)

        updated_fields = {}

        if not is_new:
            # Only check bids if it's an update
            has_bids_now = Bid.objects.filter(listing=self).exists()
            if self.has_bids != has_bids_now:
                updated_fields['has_bids'] = has_bids_now

            #Always update winner when listing is closed
            winner_now = self.highest_bidder if not self.is_active else None
            if self.winner != winner_now:
                updated_fields['winner'] = winner_now

            #Apply changes if updated_fields is not empty
            if updated_fields:
                for attr, value in updated_fields.items():
                    setattr(self, attr, value)
                Listing.objects.filter(pk=self.pk).update(**updated_fields)

    def __str__(self):
        return f"{self.title}"
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_first_bid = models.BooleanField(default=False)
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="bids", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        #validate if listing is still open
        if not self.listing.is_active:
            raise ValidationError({
                'amount': 'Cannot bid on an inactive listing'
            })
        #Validate amount must at least be the same as the starting bid
        if self.amount < self.listing.starting_bid:
            raise ValidationError({
                'amount': 'Bid amount must be at least equal to the starting bid.'
            })
        #Validate amount must be at least higher than the highest_bid, check if highest_bid exist first
        if self.listing.highest_bid is not None and self.amount <= self.listing.highest_bid:
            raise ValidationError({
                'amount': 'Bid amount must be higher than the current highest bid'
            })
        # Determine if this is the first bid
        if self.listing.bids.exists():
            self.is_first_bid = False
        else:
            self.is_first_bid = True

    def save(self, *args, **kwargs):
        #validate before saving
        self.full_clean()
        super().save(*args, **kwargs)
        #update the related listing
        self.listing.highest_bid = self.amount
        self.listing.highest_bidder = self.bidder
        self.listing.save()

    def __str__(self):
        return f"Bid: ${self.amount} by {self.bidder} on '{self.listing.title}' at {self.created_at}"
    
    
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256, null=True)
    def __str__(self):
        return f"Comment: '{self.comment}' by {self.commenter} on '{self.listing.title}'"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorited_by")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="favorites")
    def __str__(self):
        return f"'{self.user}' favorites '{self.listing}'"