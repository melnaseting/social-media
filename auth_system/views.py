from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.contrib import messages
from . import models
from .forms import UserForm, EmailPasswordForm
from django.views.generic import UpdateView, DetailView, CreateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

# Create your views here.
  
class ProfileUpdateView(UpdateView):
    model = models.Client
    form_class = UserForm
    template_name = 'auth_system/update_account.html'
    success_url = reverse_lazy('auth_system:account')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ваш профіль успішно оновлено")
        return response

def logout_view(request):
    logout(request)
    return redirect('auth_system:register')

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserForm()
    return render(
        request, 
        template_name='auth_system/register.html',
        context= {"form": form}
    )

class MyLoginView(LoginView):
    template_name = 'auth_system/login.html'

class ClientProfileView(DetailView):
    model = models.Client
    template_name = 'auth_system/account.html'
    context_object_name = 'client'

    def get_object(self):
        client_id = self.kwargs.get('client_id')
        return get_object_or_404(models.Client, id=client_id)

    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['subscribers'] = set(
                models.Subscription.objects.filter(subscriber=self.request.user).values_list('subscribed_to_id', flat=True)
            )
        else:
            context['subscribers'] = set()

        return context

class FolowUser(CreateView):
    def post(self, request,client_id, *args, **kwargs):
        client = get_object_or_404(models.Client, id=client_id)
        if client != self.request.user:
            subcription, created = models.Subscription.objects.get_or_create(
                subscriber=request.user,
                subscribed_to=client
            )
            if not created:
                subcription.delete()  
        return redirect('auth_system:account', client.id) 

def unfollow_user(request, user_id):
    to_unfollow = get_object_or_404(models.Client, id=user_id)
    models.Subscription.objects.filter(subscriber=request.user, subscribed_to=to_unfollow).delete()
    return redirect('user_profile', user_id=to_unfollow.id)
