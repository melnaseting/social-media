from django.urls import path
from . import views

app_name = 'auth_system'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('<int:client_id>/account/', views.ClientProfileView.as_view(), name='account'),
    path('<int:client_id>/account/subscribe/', views.FolowUser.as_view(),name='subscribe'),
    path('edit-profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='edit_account')
]
