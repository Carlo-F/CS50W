from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=256)
    category = models.CharField(max_length=64,blank=True,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.author} commented on {self.listing}"

class Bid(models.Model):
    amount = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_author")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="bid_listing")

    def __str__(self):
        return f"{self.author} offered {self.amount} euros on {self.listing}"