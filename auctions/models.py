from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders", null=True)
    price = models.FloatField(null=True)
    def __str__(self):
        return f"A ${self.price} bid by {self.user}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listers", null=True)
    title = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=64, null=True)
    bid = models.ForeignKey(Bid, related_name="listedBids", on_delete=models.CASCADE, null=True)
    imgURL = models.URLField(null=True)
    watchList = models.ManyToManyField(User, blank=True, related_name="watchers")
    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters", null=True)
    comment = models.CharField(max_length=128, null=True)
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"

class Category(models.Model):
    name = models.CharField(max_length=64, null=True)
    listing = models.ManyToManyField(Listing, related_name="listings", blank=True)
    def __str__(self):
        return f"{self.name}"