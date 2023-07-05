from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User

class DoctorRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    email_address = forms.EmailField()
    state = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'email_address', 'state', 'address']

class PatientRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    email_address = forms.EmailField()
    state = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'email_address', 'state', 'address']
        


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email_address', 'state', 'address', 'photo')
