from django.contrib import admin

from .models import *
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "seller", "is_active", "winner", "category")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "image_url")
    filter_horizontal = ("watchlist",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "amount", "listing")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "image_url", "description")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("commenter", "comment", "listing")

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)