from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    tag = models.CharField(max_length=64)
    def __str__(self):
            return self.tag

class Listing(models.Model):
    name= models.CharField(max_length=64)
    description= models.TextField(max_length=600)
    img= models.CharField(max_length=100)
    price= models.FloatField()
    isListed= models.BooleanField(default=True)
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name='all_listed_items') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null = True, related_name='all_products')

    def __str__(self):
        return f"{self.name} listed by {self.listedBy}"
