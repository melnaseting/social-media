from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import Form, EmailField, EmailInput, CharField, PasswordInput, TextInput, ChoiceField, ModelChoiceField, Select
from . import models

class UserForm(UserCreationForm):
    password1 = CharField(
        label="Пароль",
        widget=PasswordInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Придумайте пароль',
            'id': 'id_password1',
            'data-toggle': 'password',
        })
    )
    password2 = CharField(
        label="Повторіть пароль",
        widget=PasswordInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Повторіть пароль',
            'id': 'id_password1',
            'data-toggle': 'password',
        })
    )

    class Meta:
        model =  models.Client
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control email',
                'placeholder': 'Імя користувача',
            }),
            "email": EmailInput(attrs={
                'class': 'form-control email',
                'placeholder': 'Ваша пошта',
            }),
        }

class EmailPasswordForm(Form):
    email = EmailField(
        label="Електронна пошта", 
        widget=EmailInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Ваша пошта',
        })
    )
    password = CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Пароль',
            'id': 'id_password',
            'data-target': 'id_password'
        }),
        label="Пароль"
    )

    user = ModelChoiceField(
        queryset= models.Client.objects.all(), 
        label="Оберіть користувача",
        widget=Select(attrs={'class': 'form-select'})
    )
    group = ModelChoiceField(
        queryset=Group.objects.all(), 
        label="Оберіть групу",
        widget=Select(attrs={'class': 'form-select'})
    )