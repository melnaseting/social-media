from django.db import models
from django.contrib.auth.models import AbstractUser
from posts.models import Post

class Client(AbstractUser):
    photo = models.ImageField(
        upload_to='media/',
        default='media\profile_photo.png'
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=150
    )

    def get_posts_count(self):
        return Post.objects.filter(created_by = self).count()

    def get_subscribers_count(self):
        return Subscription.objects.filter(subscribed_to=self).count()

    def get_subscriptions_count(self):
        return Subscription.objects.filter(subscriber=self).count()
    
    def has_unread_messages(self):
        return Message.objects.filter(message_to = self, read = False)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Сохраняем флаг: пользователь новый?
        super().save(*args, **kwargs)

        if is_new:
            from messenger.models import ChatGroup  # Импорт внутри метода, чтобы избежать циклов
            group, created = ChatGroup.objects.get_or_create(group_name='public-chat')
            group.members.add(self)

class Subscription(models.Model):
    subscriber = models.ForeignKey(
        Client,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    subscribed_to = models.ForeignKey(
        Client,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')  # щоб уникнути дублювання підписок

    def __str__(self):
        return f"{self.subscriber.username} → {self.subscribed_to.username}"

class Message(models.Model):
    text = models.TextField()
    message_to = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='message_to'
    )
    message_from = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='message_from'
    )
    created_time = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100,default='None')
