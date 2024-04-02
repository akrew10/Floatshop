

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Wear(models.Model): 
    WearName = models.CharField(max_length=15)
    def __str__(self):
        return  self.WearName

class Category(models.Model): 
    categoryName = models.CharField(max_length=64)
    def __str__(self):
        return self.categoryName
    
class bid(models.Model):
    bidprice = models.FloatField(default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")


    def __str__(self):
        return self.bidprice


class Listing(models.Model):
    
    title = models.CharField(max_length = 256)
    float = models.FloatField()
    startprice = models.ForeignKey(bid, on_delete=models.CASCADE, blank=True, null=True, related_name="startprice")
    buyprice = models.FloatField()
    photo = models.CharField(max_length = 1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    wear = models.ForeignKey(Wear, on_delete=models.CASCADE, blank=True, null=True, related_name="wear")
    Active = models.BooleanField(default=True)
    StatTrak = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank = True,null=True, related_name="watchinglist")
    def __str__(self):
        return self.title
    
    

class Comment(models.Model):
    comment = models.CharField(max_length = 500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="usercomment")
    comments = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    def __str__(self):
        return f"{self.author}'s comment on {self.comments}"
    

