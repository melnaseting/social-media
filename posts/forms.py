from django import forms
from . import models

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['photo', 'description']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control',"type":"file","accept":"image/png, image/jpeg"}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Опис'}),
        }

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'comment_field', 'placeholder': 'Коментар'}),
        }
