from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='posts'),
    path('detail/<int:pk>',views.PostDetailView.as_view(), name='post_detail'),
    path('like/<int:post_id>/', views.ToggleLikeView.as_view(), name='like_post'),
    path('create/', views.CreatePostView.as_view(), name="create_post"),
    path('delete/<int:pk>', views.DeletePostView.as_view(), name="delete_post"),
    path('send-comment/<int:pk>', views.CreateCommentView.as_view(), name="send_comment"),
]