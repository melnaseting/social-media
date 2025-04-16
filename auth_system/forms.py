from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms
from . import models

class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ['email', 'username','description','photo']
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
            'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
            'description' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Опис'}),
            'photo' : forms.FileInput(attrs={'class': 'form-control',"type":"file","accept":"image/png, image/jpeg"})
        }

class ClientRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторіть пароль'}))
    class Meta:
        model = models.Client
        fields = ['username', 'email', 'password', 'password2']
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
            'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
            }
        
class ClientLoginForm(forms.Form):
    username = forms.CharField(
        label="Нікнейм", 
        widget=forms.TextInput(attrs={
             'class': 'form-control email',
             'placeholder': 'Нікнейм',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
             'class': 'form-control email',
             'placeholder': 'Пароль',
            'id': 'id_password',
            'data-target': 'id_password'
        }),
        label="Пароль"
    )