from django.db import models
from auth_system.models import Client

# Create your models here.
class Post(models.Model):
    created_by = models.ForeignKey(Client,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/', height_field=None, width_field=None,null=True)
    description = models.TextField(null=True,blank=True)
    created_time = models.DateTimeField(auto_now=True)

    def like_count(self):
        return self.like_set.count()

    def is_liked_by(self, user):
        return self.like_set.filter(user=user).exists()

class Like(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    created_by = models.ForeignKey(Client,on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    created_time = models.DateTimeField(auto_now=True)
