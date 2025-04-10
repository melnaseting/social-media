from django.urls import path
from . import views

app_name = 'auth_system'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.request_login, name='login'),
    path('account/', views.ProfileAboutView.as_view(), name='account'),
    path('edit-profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='edit_account')

]