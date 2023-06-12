from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.content}' by {self.user.username}"

class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.user.username}' is following {self.following_user.username}"
    
class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    liked_post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likers")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.user.username}' likes {self.liked_post}"