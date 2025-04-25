from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from . import models
from posts.forms import CreateCommentForm
from posts.models import Comment, Post, Like
from .forms import ClientForm, ClientRegistrationForm, ClientLoginForm, ClientFilterForm
from django.views.generic import UpdateView, DetailView, CreateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
  
def logout_view(request):
    logout(request)
    return redirect('auth_system:login')

class RegisterView(CreateView):
    model = models.Client
    form_class = ClientRegistrationForm
    template_name = 'auth_system/register.html'
    success_url = reverse_lazy('posts:posts')  

    def form_valid(self, form):
        messages.success(self.request, "Ви успішно зареєстровані! Тепер увійдіть у свій акаунт.")
        return super().form_valid(form)

class ClientLoginView(View):
    template_name = 'auth_system/login.html'
    form_class = ClientLoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('posts:posts')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})

    

    def form_valid(self, form):
        messages.success(self.request, f"Вітаємо, {form.get_user().username}!")
        return super().form_valid(form)

class ClientListView(ListView):
    model = models.Client
    template_name = 'auth_system/client_list'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()

        username = self.request.GET.get("username","")
        if username:
            queryset = queryset.filter(username__icontains=username)
        
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ClientFilterForm(self.request.GET)
        return context

class ClientProfileView(DetailView):
    model = models.Client
    template_name = 'auth_system/account.html'
    context_object_name = 'client'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(models.Client, id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()

        unread_messages = models.Message.objects.filter(message_to = self.request.user,read = False)
        if unread_messages:
            messages.info(self.request, 'У вас нове повідомлення, перегляньте у розділі "Повідомлення"')

        if self.request.user.is_authenticated and self.request.user != client:
            is_subscribed = models.Subscription.objects.filter(
                subscriber=self.request.user,
                subscribed_to=client
            ).exists()
            context['is_subscribed'] = is_subscribed
        else:
            context['is_subscribed'] = False

        context['posts'] = Post.objects.filter(
            created_by = client
        )

        context['comments'] = Comment.objects.all()
        context["form"] = CreateCommentForm()
        if self.request.user.is_authenticated:
            context['liked_posts'] = set(
                Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            )
        else:
            context['liked_posts'] = set()
        return context

class ProfileUpdateView(UpdateView):
    model = models.Client
    form_class = ClientForm
    template_name = 'auth_system/update_account.html'
    
    def get_success_url(self):
        return reverse('auth_system:account', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ваш профіль успішно оновлено")
        return response

class FolowUser(LoginRequiredMixin,CreateView):
    def post(self, request,pk, *args, **kwargs):
        client = get_object_or_404(models.Client, id=pk)
        if client != self.request.user:
            subcription, created = models.Subscription.objects.get_or_create(
                subscriber=request.user,
                subscribed_to=client
            )
            if not created:
                subcription.delete()  
            else:
                message = models.Message.objects.create(
                    text = f'{subcription.subscriber} почав слідкувати за вами',
                    message_to = subcription.subscribed_to,
                    message_from = subcription.subscriber,
                    category = 'folowed_user'
                )
        return redirect('auth_system:account', client.id) 

class MessageListView(LoginRequiredMixin, ListView):
    model = models.Message
    template_name = 'auth_system/messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        client = self.request.user
        queryset =  models.Message.objects.filter(message_to=client)
        return queryset.order_by('-created_time')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # Помічаємо як прочитані
        client = self.request.user
        models.Message.objects.filter(message_to=client, read=False).update(read=True)

        return response

class DeleteMessagesView(View):
    def post(self, request, *args, **kwargs):
        client_id = request.user
        if client_id:
            models.Message.objects.filter(message_to_id=client_id).delete()
        return redirect('auth_system:messages')