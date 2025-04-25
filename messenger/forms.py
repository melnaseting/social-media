from django import forms
from . import models

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = models.GroupMessage
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Надіслати повідомлення...', 'class':'message_input','autofocus':True})
        }