from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User

class DoctorRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    email_address = forms.EmailField()
    state = forms.CharField(max_length=100)
    location = forms.CharField(max_length=255)

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



class DoctorProfileForm(UserChangeForm):
    EMPLOYMENT_CHOICES = [
        ('Private', 'Private'),
        ('Government', 'Government'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    specialty = forms.CharField(max_length=100)
    #experience_years = forms.IntegerField()
    current_employment = forms.ChoiceField(choices=EMPLOYMENT_CHOICES)
    #certifications = forms.CharField(max_length=200)
    medical_license_number = forms.CharField(max_length=20)
    nationality = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email_address', 'state', 'address', 'photo', 'specialty', \
         'years_of_experience', 'current_employment', 'professional_certifications', 'medical_license_number', 'nationality')
