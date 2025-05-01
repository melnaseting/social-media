from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from . import models
import json

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(models.ChatGroup, group_name = self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        
        #Створення та оновлення онлайн користувачів
        if self.user not in self.chatroom.client_online.all():
            self.chatroom.client_online.add(self.user)
            self.update_online_count()

        self.accept()
        
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )
        #Видалення та оновлення онлайн користувачів
        if self.user in self.chatroom.client_online.all():
            self.chatroom.client_online.remove(self.user)
            self.update_online_count() 
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['text']

        message = models.GroupMessage.objects.create(
            text = text,
            author = self.user,
            group = self.chatroom
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = models.GroupMessage.objects.get(id=message_id)
        html = render_to_string('messenger/partials/chat_message_p.html', {'message': message, 'user': self.user})
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.client_online.count()-1
        
        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
        
    def online_count_handler(self, event):
        online_count = event['online_count']      

        context = {
            'online_count': online_count,
            'chat_group': self.chatroom,
        }
        html = render_to_string("messenger/partials/online_count.html", context)
        self.send(text_data=html) 