from django.db import models
from auth_system.models import Client
import shortuuid
from random import randint

default_group_imeges=[
    'media/chat_group_images/0.png',
    'media/chat_group_images/1.png',
    'media/chat_group_images/2.png',
    'media/chat_group_images/3.png',
    'media/chat_group_images/4.png',
    'media/chat_group_images/5.png'
]

def generate_unique_invite_code():
    return shortuuid.uuid()[:10]

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique = True, default=shortuuid.uuid)
    photo = models.ImageField(upload_to='media/',default=default_group_imeges[randint(0,5)])
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(Client, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    client_online = models.ManyToManyField(Client, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(Client, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    invite_code = models.CharField(max_length=16, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self._generate_unique_invite_code()
        super().save(*args, **kwargs)

    def _generate_unique_invite_code(self):
        while True:
            code = shortuuid.uuid()[:10]
            if not ChatGroup.objects.filter(invite_code=code).exists():
                return code

    def __str__(self):
        return self.group_name
    
    def get_members_count(self):
        return self.members.count()
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(Client, models.CASCADE)
    text  = models.CharField(max_length=300)
    created_time = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.author.username} : {self.text}'
    
    class Meta:
        ordering = ['-created_time']