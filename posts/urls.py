from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='posts'),
    path('like/<int:post_id>/', views.ToggleLikeView.as_view(), name='like_post'),

]