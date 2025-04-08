from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models

# Create your views here.
class PostsListView(ListView):
    model = models.Post
    template_name = "posts/posts_list.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            like.delete()  # убираем лайк, если уже был
        return redirect('posts:posts')