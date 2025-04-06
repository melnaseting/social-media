from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import Form, EmailField, EmailInput, CharField, PasswordInput, TextInput, ChoiceField, ModelChoiceField, Select

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
        model = User
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

class ChooseUserForm(Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = User.objects.exclude(id=user.id)

    user = ModelChoiceField(
        queryset=User.objects.all(), 
        label="Оберіть користувача",
        widget=Select(attrs={'class': 'form-select'})
    )
    group = ModelChoiceField(
        queryset=Group.objects.all(), 
        label="Оберіть групу",
        widget=Select(attrs={'class': 'form-select'})
    )