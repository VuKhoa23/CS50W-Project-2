from django.contrib import admin
from .models import User, Listing, Category, CommentOnListing
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(CommentOnListing)