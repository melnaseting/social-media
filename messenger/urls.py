from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('messenger/',views.ChatListView.as_view(),name='messenger'),
    path('start-chat/<username>', views.get_or_create_chatroom, name="start-chat"),
    path('chat/<chatroom_name>', views.chat_view, name='chatroom'),
    
]