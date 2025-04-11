from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='posts'),
    path('like/<int:post_id>/', views.ToggleLikeView.as_view(), name='like_post'),
    path('create/', views.CreatePostView.as_view(), name="create_post"),
    path('send-comment/<int:pk>', views.CreateCommentView.as_view(), name="send_comment"),
]