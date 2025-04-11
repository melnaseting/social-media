from django.views.generic import ListView, View, CreateView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from . import models, forms
from django.contrib import messages
import uuid
import base64

# Create your views here.
class PostsListView(ListView):
    model = models.Post
    template_name = "posts/posts_list.html"
    context_object_name = "posts"
    ordering = '-created_time'

    def get_context_data(self, **kwargs):
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
    
class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(models.Post, id=post_id)
        like, created = models.Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()  
        return redirect('posts:posts')
    
class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = forms.CreatePostForm 
    model  = models.Post
    template_name = "posts/create_post.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = self.request.user
            post.save()

            messages.success(request, 'Пост додано, перегляньте сторінку.')
            return redirect('posts:posts')

        # если форма невалидна — возвращаем страницу с формой и ошибками
        return render(request, self.template_name, {'form': form})

class CreateCommentView(LoginRequiredMixin,CreateView):
    model = models.Comment()
    def post(self, request, *args, **kwargs):
        comment = models.Comment.objects.create(
            text = request.POST['text'],
            created_by = request.user,
            post = models.Post.objects.get(pk = kwargs['pk']))           
        return redirect('posts:posts')