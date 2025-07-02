from mptt.admin import DraggableMPTTAdmin
from django.contrib import admin

from .models import *
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "seller", "is_active", "winner")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "balance")
    filter_horizontal = ("watchlist",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "amount", "listing")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Favorite)