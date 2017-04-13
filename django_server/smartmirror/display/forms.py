from django.contrib.auth.models import User
from django import forms

from accounts.models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bus_stop','zip_code','metric_units','time_zone')