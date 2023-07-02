from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, authenticate
from .forms import DoctorRegistrationForm, PatientRegistrationForm
from django.contrib.auth.decorators import login_required

# All views here
def index(request):
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 'doctor':
            # Logic for doctors
            return redirect('doctor_dashboard')
        elif user_type == 'patient':
            # Logic for patients
            return redirect('patient_dashboard')
        else:
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')


def about_us(request):
    return render(request, 'about.html')


def doctor_registration(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'doctor'
            user.save()
            
            # Log the user in
            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('doctor_home')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'accounts/doctor_registration.html', {'form': form})


def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_type = 'patient'
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'accounts/patient_registration.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('home')
        else:
            # Handle invalid login
            pass
    return render(request, 'accounts/login.html')


@login_required
def doctor_dashboard(request):
    # Retrieve the authenticated doctor user
    doctor = request.user
    context = {
        'doctor': doctor,
        #'patients': patients,
    }

    return render(request, 'doctor_dashboard.html', context)



@login_required
def patient_dashboard(request):
    patient = request.user
    context = {
        'patient': patient,
        #'patients': patients,
    }

    return render(request, 'patient_dashboard.html', context)