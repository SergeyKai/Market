from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Profile

User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    password = None


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
