from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User, Group
from .forms import UserForm, EmailPasswordForm, ChooseUserForm
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
import core.settings
# Create your views here.

class ProfileAboutView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'auth_system/account.html'
    context_object_name = 'account_detail'

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChooseUserForm(user=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = ChooseUserForm(request.POST)
        if form.is_valid():
            userr = form.cleaned_data['user']
            group_now = userr.groups.first()
            if group_now:
                userr.groups.remove(group_now)
            groupp = form.cleaned_data['group']

            userr.groups.add(groupp)
            messages.success(request, f'Користувача {userr.username} успішно додано до {groupp.name}.')
            return redirect('auth_system:account')
        messages.error(request, 'Щось пішло не так, спробуйте пізніше')
        return render(request, 'auth_system/account.html', {'form': form, 'account_detail': self.get_object()})



class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'auth_system/update_account.html'
    success_url = reverse_lazy('auth_system:account')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ваш профіль успішно оновлено")
        return response

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserForm()
    return render(
        request, 
        template_name='auth_system/register.html',
        context= {"form": form}
    )

def request_login(request):
    if request.method == 'POST':
        form = EmailPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Перевірка користувача
            try:
                admin = User.objects.get(email=email)
                if admin.check_password(password):
                    login(request, admin)
                    request.session['username'] = admin.username
                    subject = admin.username
                    message = f'Вітаємо, {subject}. Ви успішно увійшли в свій акаунт! Ми раді вас бачити'
                    from_email = core.settings.EMAIL_HOST_USER
                    to_email = admin.email
                    send_mail(
                        subject,
                        message,
                        from_email, 
                        [to_email],
                        fail_silently=False
                    )
                    return redirect('home')
                else:
                    messages.error(request, 'Невірний пароль!')
                    return redirect('auth_system:login')
            except User.DoesNotExist:
                messages.error(request, 'Користувач або адмін з таким email не знайдено.')
                return redirect('auth_system:login')

    else:
        form = EmailPasswordForm()
    return render(request, 'auth_system/request_login.html', {'form': form})