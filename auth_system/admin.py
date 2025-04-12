from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, Subscription

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