from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, Q, Count
from django.http  import HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from . import models
from .import forms
from auth_system.models import Client
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(models.ChatGroup, group_name=chatroom_name)
    chat_messages = models.GroupMessage.objects.filter(group=chat_group)
    form = forms.MessageCreateForm()
    members = chat_group.members.all()
    other_user = None

    if chatroom_name == 'public-chat':
        for client in Client.objects.all():
            chat_group.members.add(client)
    
    # Проверка доступа
    if request.user not in members:
        raise Http404("Ви не є учасником цього чату")

    # Определение другого участника для приватных чатов
    if chat_group.is_private:
        for member in members:
            if member != request.user:
                other_user = member
                break

    for client in chat_group.members.all():
        if client.username == 'adding_message':
            chat_group.members.remove(client)

    # Обработка отправки сообщения
    if request.method == 'POST':
        if request.user not in chat_group.members.all():
            return HttpResponse(status=403)

        form = forms.MessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            if request.headers.get('HX-Request'):
                html = render_to_string('messenger/partials/chat_message_p.html', {'message': message, 'user': request.user})
                return HttpResponse(html)

            return redirect('messenger:chatroom', chatroom_name)

    return render(request, "messenger/chat.html", {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'members': members,
        'chat_group': chat_group
    })

@login_required
def confirm_join(request, chatroom_name):
    chat_group = get_object_or_404(models.ChatGroup, group_name=chatroom_name)

    if request.user in chat_group.members.all():
        return redirect('messenger:chatroom', chatroom_name)

    if chat_group.is_private:
        raise Http404()

    chat_group.members.add(request.user)
    models.GroupMessage.objects.create(
        group=chat_group,
        author=get_object_or_404(Client, username='adding_message'),
        text=f'{request.user.username} приєднався до групи'
    )
    return redirect('messenger:chatroom', chatroom_name)


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

class ChatListView(LoginRequiredMixin,ListView):
    model = models.ChatGroup
    template_name = 'messenger/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return models.ChatGroup.objects.annotate(
            last_msg_time=Max('chat_messages__created_time'),
            num_members=Count('members')
        ).exclude(
            Q(is_private=True) & Q(num_members__lte=1)
        ).exclude(
            Q(is_private=True) & Q(members__username='adding_message')
        ).order_by('-last_msg_time')

@login_required
def create_groupchat(request):
    form = forms.GroupCreateForm()
    
    if request.method == 'POST':
        form = forms.GroupCreateForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('messenger:chatroom', new_groupchat.group_name)
    
    context = {
        'form': form
    }
    return render(request, 'messenger/create_groupchat.html', context)

@login_required
def chatroom_edit_view(request, group_name):
    chat_group = get_object_or_404(models.ChatGroup, group_name=group_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    form = forms.ChatRoomEditForm(instance=chat_group) 
    
    if request.method == 'POST':
        form = forms.ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = Client.objects.get(id=member_id)
                chat_group.members.remove(member)  
                models.GroupMessage.objects.create(
                    group = chat_group,
                    author = get_object_or_404(Client, username='adding_message'),
                    text = f'{member} був видалений'
                )
                
            return redirect('messenger:chatroom', group_name) 
    
    context = {
        'form' : form,
        'chat_group' : chat_group
    }   
    return render(request, 'messenger/edit_chat.html', context) 

@login_required
def add_client(request,invite_code):
    group = get_object_or_404(models.ChatGroup, invite_code = invite_code)
    if request.user not in group.members.all():
        group.members.add(request.user)
        models.GroupMessage.objects.create(
            group = group,
            author = get_object_or_404(Client, username='adding_message'),
            text = f'{request.user} приєднався до чату'
        )
    return redirect('messenger:chatroom', group.group_name) 

@login_required
def leave_group(request, chatroom_name):
    group = get_object_or_404(models.ChatGroup, group_name = chatroom_name)
    if request.user in group.members.all() and chatroom_name!='public-chat':
        if request.user != group.admin:
            group.members.remove(request.user)
            models.GroupMessage.objects.create(
                group = group,
                author = get_object_or_404(Client, username='adding_message'),
                text = f'{request.user} користувач покинув чат'
            )
        else:
            group.delete()
        return redirect('messenger:messenger')
