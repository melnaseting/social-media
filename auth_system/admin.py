from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, Subscription, Message

@admin.register(Client)
class ClientAdmin(UserAdmin):
    model = Client
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ("Додатково", {
            'fields': ('photo', 'description')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Додатково", {
            'fields': ('photo', 'description')
        }),
    )

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to', 'created_at')
    search_fields = ('subscriber__username', 'subscribed_to__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    # Опційно: для відображення при додаванні підписки можна налаштувати поля в form
    fieldsets = (
        (None, {
            'fields': ('subscriber', 'subscribed_to', 'created_at')
        }),
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_short', 'message_from', 'message_to', 'created_time', 'read')
    list_filter = ('read', 'created_time')
    search_fields = ('text', 'message_from__name', 'message_to__name')
    autocomplete_fields = ('message_from', 'message_to')
    readonly_fields = ('created_time',)

    def text_short(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_short.short_description = 'Text'