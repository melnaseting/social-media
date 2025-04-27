from django.db import models
from auth_system.models import Client
import shortuuid

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique = True, default=shortuuid.uuid)
    client_online = models.ManyToManyField(Client, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(Client, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(Client, models.CASCADE)
    text  = models.CharField(max_length=300)
    created_time = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.author.username} : {self.text}'
    
    class Meta:
        ordering = ['-created_time']