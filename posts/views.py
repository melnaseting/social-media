from django.views.generic import ListView, View, CreateView, DeleteView, DetailView
from django.urls import resolve
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from . import models, forms
from django.contrib import messages
import uuid
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
import base64
from django.http import HttpResponseRedirect
from auth_system.models import Message, Client, Subscription
from django.db.models import Case, When, Value, IntegerField, Q


# Create your views here.
class PostsListView(ListView):
    model = models.Post
    template_name = "posts/posts_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user
        qs = models.Post.objects.all()

        if user.is_authenticated:
            subscriptions = Subscription.objects.filter(subscriber=user).values_list('subscribed_to_id', flat=True)

            qs = qs.filter(~Q(created_by=user))  # Исключаем посты текущего пользователя
            qs = qs.annotate(
                is_followed=Case(
                    When(created_by__in=subscriptions, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by('-is_followed', '-created_time')

        else:
            qs = qs.order_by('-created_time')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            unread_messages = Message.objects.filter(message_to = self.request.user,read = False)
            if unread_messages:
                messages.info(self.request, 'У вас нове повідомлення, перегляньте у розділі "Повідомлення"')
        context['comments'] = models.Comment.objects.all()
        context["form"] = forms.CreateCommentForm()
        if self.request.user.is_authenticated:
            context['liked_posts'] = set(
                models.Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            )
        else:
            context['liked_posts'] = set()
        return context

class PostDetailView(DetailView):
    model = models.Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        unread_messages = Message.objects.filter(message_to = self.request.user,read = False)
        if unread_messages:
            messages.info(self.request, 'У вас нове повідомлення, перегляньте у розділі "Повідомлення"')
        context = super().get_context_data(**kwargs)
        context['comments'] = models.Comment.objects.all()
        context["form"] = forms.CreateCommentForm()
        if self.request.user.is_authenticated:
            context['liked_posts'] = set(
                models.Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            )
        else:
            context['liked_posts'] = set()
        return context

class DeletePostView(DeleteView):
    model = models.Post
    template_name = 'posts/delete_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_messages = Message.objects.filter(message_to = self.request.user,read = False)
        if unread_messages:
            messages.info(self.request, 'У вас нове повідомлення, перегляньте у розділі "Повідомлення"')
        
        next_url = self.request.POST.get('next') or self.request.META.get('HTTP_REFERER', '/')

        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            next_url = '/'
        context['return_url'] = next_url
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return_url = request.POST.get('return_url', '/')
        self.object.delete()
        return HttpResponseRedirect(return_url)
    
class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = forms.CreatePostForm 
    model  = models.Post
    template_name = "posts/create_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_messages = Message.objects.filter(message_to = self.request.user,read = False)
        if unread_messages:
            messages.info(self.request, 'У вас нове повідомлення, перегляньте у розділі "Повідомлення"')
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()

            for client in Subscription.objects.filter(subscribed_to=self.request.user):
                message = Message.objects.create(
                    text = f'{request.user} створив новий пост',
                    message_to = client.subscriber,
                    message_from = request.user,
                    post = post,
                    category = 'created_post'
                )

            messages.success(request, 'Пост додано, перегляньте сторінку.')
            return redirect('posts:posts')

        return render(request, self.template_name, {'form': form})

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(models.Post, id=post_id)
        like, created = models.Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        elif request.user != like.post.created_by:
            Message.objects.create(
                text=f'{like.user} вподобав ваш пост',
                message_to=like.post.created_by,
                message_from=request.user,
                post=post,
                category='liked_post'
            )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            liked_posts = set(
                models.Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            )
            html = render_to_string('posts/partials/like_block.html', {
                'post': post,
                'liked_posts': liked_posts
            }, request=request)
            return HttpResponse(html)

        return redirect(request.POST.get('next', '/'))
       
class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['pk'])
        comment = models.Comment.objects.create(
            text=request.POST['text'],
            created_by=request.user,
            post=post
        )
        if post.created_by != request.user:
            Message.objects.create(
                text=f'{comment.created_by} надіслав вам коментар "{comment.text[:10]}…" ',
                message_to=post.created_by,
                message_from=request.user,
                post=post,
                category='created_comment'
            )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            comments = models.Comment.objects.filter(post=post)  
            html = render_to_string('posts/partials/comments_block.html', {
                'comments': comments,
                'post': post
            }, request=request)
            return HttpResponse(html)

        return redirect(request.POST.get('next', '/'))     
        