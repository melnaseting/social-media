from django.db import models
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    photo = models.ImageField(
        upload_to='media/',
        null=True,
        blank=True,
        default='static\profile_photo.png'
    )
    description = models.TextField(
        null=True,
        blank=True
    )

    def get_subscribers_count(self):
        return Subscription.objects.filter(subscribed_to=self).count()

    def get_subscriptions_count(self):
        return Subscription.objects.filter(subscriber=self).count()

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
