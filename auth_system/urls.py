from django.urls import path
from . import views

app_name = 'auth_system'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.ClientLoginView.as_view(), name='login'),
    path('client-list/', views.ClientListView.as_view(),name="client_list"),
    path('<int:pk>/account/', views.ClientProfileView.as_view(), name='account'),
    path('<int:pk>/account/subscribe/', views.FolowUser.as_view(),name='subscribe'),
    path('<int:pk>/account/edit/', views.ProfileUpdateView.as_view(), name='edit_account'),
    path('messages/',views.MessageListView.as_view(), name='messages'),
    path('messages/delete/', views.DeleteMessagesView.as_view(), name='delete_messages'),
]
