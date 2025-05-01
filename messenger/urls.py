from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('messenger/', views.ChatListView.as_view(), name='messenger'),
    path('chat/new-groupchat/', views.create_groupchat, name="new_groupchat"),  
    path('start-chat/<username>/', views.get_or_create_chatroom, name="start-chat"),
    path('chat/<chatroom_name>/', views.chat_view, name='chatroom'),
    path('chat/edit/<group_name>', views.chatroom_edit_view, name='edit_chatroom')
]
