from django.contrib.auth.models import User
from django import forms

from accounts.models import UserProfile
# from .models import Calendar, Mirror


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('time_zone', 'bus_stop', 'zip_code', 'metric_units', 'ical_link')
        widgets = {
            'ical_link': forms.TextInput(attrs={'size':'40'}),
        }


# class BusStopForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('bus_stop',)

# class WeatherForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('zip_code','metric_units')

# class CalendarForm(forms.ModelForm):
#     # user = forms.ModelChoiceField(label="",
#     #                               queryset=UserProfile.objects.all(),
#     #                               widget=forms.HiddenInput())
#     class Meta:
#         model = UserProfile
#         fields = ('ical_link')
#         # widgets = {'user': forms.HiddenInput()}

# class MirrorForm(forms.ModelForm):
#     # user = forms.ModelChoiceField(label="",
#     #                               queryset=UserProfile.objects.all(),
#     #                               widget=forms.HiddenInput())
#     class Meta:
#         model = Mirror
#         fields = ('name','user')
#         widgets = {'user': forms.HiddenInput()}

