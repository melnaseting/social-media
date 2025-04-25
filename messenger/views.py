from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import models
from .import forms

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(models.ChatGroup, group_name='Chat1')
    chat_messages = models.GroupMessage.objects.filter(group = chat_group)
    form = forms.MessageCreateForm()

    if request.htmx:
        form = forms.MessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user' : request.user,
            }
            return render(request, "messenger/partials/chat_message_p.html", context)

    return render(request, "messenger/chat.html", {'chat_messages':chat_messages,'form' : form})