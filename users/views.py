from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegistrationForm, NewRegistrationForm, CustomPasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from samplesite.settings import LOGIN_REDIRECT_URL
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = NewRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            context = {"title": "Регистрация завершена", "new_user": new_user}
            return render(request, template_name="users/registration_done.html", context=context)
    form = NewRegistrationForm()
    context = {"title": "Регистрация пользователя", "register_form": form}
    return render(request, template_name="users/registration.html", context=context)

def log_in(request):
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            url = request.GET.get('next', LOGIN_REDIRECT_URL)
            return redirect(url)
    context = {'form': form}
    return render(request, template_name='users/login.html', context=context)

@login_required
def log_out(request):
    logout(request)
    return redirect('bboard:index')

@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        raise PermissionDenied()
    context = {'user': user, 'title': 'Информация о пользователе'}
    return render(request, template_name='users/profile.html', context=context)

@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            if not request.user.check_password(old_password):
                messages.error(request, "Старый пароль неверный")
            else:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Ваш пароль успешно изменен")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, template_name='users/change_password.html', context={"form": form})