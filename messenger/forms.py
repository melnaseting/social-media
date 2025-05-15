from django import forms
from . import models

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = models.GroupMessage
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Надіслати повідомлення...',
                'class':'message_input','autofocus':True
                })
        }

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = models.ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Назва групи',
                'class':'form-control','autofocus':True,
                'maxlength' : '300', 
                })
        }

class ChatRoomEditForm(forms.ModelForm):
    class Meta:
        model = models.ChatGroup
        fields = ['groupchat_name','photo']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength' : '300', 
                }),
            'photo' : forms.FileInput(attrs={
                'class': 'form-control',
                "type":"file","accept":"image/png, image/jpeg"
                })
        }