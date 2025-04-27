from django.shortcuts import render, get_object_or_404, redirect
from django.http  import HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from . import models
from .import forms
from auth_system.models import Client
from django.views.generic.list import ListView

# Create your views here.

@login_required
def chat_view(request, chatroom_name = 'public-chat'):
    chat_group = get_object_or_404(models.ChatGroup, group_name=chatroom_name)
    chat_messages = models.GroupMessage.objects.filter(group=chat_group)
    form = forms.MessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.method == 'POST':
        form = forms.MessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            if request.headers.get('HX-Request'):
                html = render_to_string('messenger/partials/chat_message_p.html', {'message': message, 'user': request.user})
                return HttpResponse(html)

            return redirect('messenger:chat')

    return render(request, "messenger/chat.html", {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name
    })

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('auth_system:account', request.user.id)

    other_user = get_object_or_404(Client, username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    for chatroom in my_chatrooms:
        if other_user in chatroom.members.all():
            return redirect('messenger:chatroom', chatroom_name=chatroom.group_name)

    # Якщо не знайшли спільний чат — створюємо
    chatroom = models.ChatGroup.objects.create(is_private=True)
    chatroom.members.add(other_user, request.user)

    return redirect('messenger:chatroom', chatroom_name=chatroom.group_name)

class ChatListView(ListView):
    model = models.ChatGroup
    template_name = 'messenger/chat_list'
    context_object_name = 'chats'