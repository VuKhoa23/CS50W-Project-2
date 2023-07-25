from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    tag = models.CharField(max_length=64)
    def __str__(self):
            return self.tag

class Bid(models.Model):
     bid_price = models.FloatField(default=0)
     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null = True, related_name="all_bids")
     def __str__(self):
            return f"${self.bid_price} by {self.user}"

class Listing(models.Model):
    name= models.CharField(max_length=64)
    description= models.TextField(max_length=600)
    img= models.CharField(max_length=300)
    price= models.FloatField()
    isListed= models.BooleanField(default=True)
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name='all_listed_items') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null = True, related_name='all_products')
    watchlist = models.ManyToManyField(User, blank = True, null = True, related_name='user_watchlist')
    placed_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank = True, null = True, related_name="all_placed_bid")
    def __str__(self):  
        return f"{self.name} listed by {self.listedBy}"

class CommentOnListing(models.Model):
     author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null = True, related_name='user_comments')
     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null = True, related_name='listing_comments')
     comment = models.TextField(max_length=600)

     def __str__(self):
          return f"{self.author} : {self.comment}"
     

    
