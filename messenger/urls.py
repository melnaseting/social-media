from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('messenger/',views.chat_view,name='chat'),
]