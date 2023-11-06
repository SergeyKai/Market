from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import CustomUserChangeForm, ChangeProfileForm
from .models import Profile

from cart.models import Cart


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            Cart.objects.create(user=user)
            login(request, user)
            return redirect('profile')

    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'user/login.html', {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        pass

    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'user/profile.html', {'profile': user_profile})


@login_required()
def user_change_data(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'user/change_data.html', {'form': form})


@login_required()
def user_logout(request):
    logout(request)
    return redirect('login')
