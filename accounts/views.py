from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, authenticate
from .forms import DoctorRegistrationForm, PatientRegistrationForm, UserProfileForm, DoctorProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from diagnosis.utils import is_patient, is_doctor
from medical_records.models import MedicalHistory
from diagnosis.models import PatientDiagnosis

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
@user_passes_test(is_doctor, login_url='login')
def doctor_dashboard(request):
    # Retrieve the authenticated doctor user
    doctor = request.user
    patient_diagnosis = PatientDiagnosis.objects.all()
    context = {
        'doctor': doctor,
        'patient_diagnosis':patient_diagnosis
        #'patients': patients,
    }

    return render(request, 'doctor_dashboard.html', context)



@login_required
@user_passes_test(is_patient, login_url='login')
def patient_dashboard(request):
    patient = request.user
    medical_records = MedicalHistory.objects.filter(patient=patient)
    patient_diagnoses = PatientDiagnosis.objects.filter(patient=patient)
    context = {
        'patient': patient,
        'medical_records':medical_records,
        'patient_diagnoses': patient_diagnoses
    }

    return render(request, 'patient_dashboard.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        print('Post Request:', request.POST) 
        print('File Request:', request.FILES)
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            user = request.user
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})


@login_required
def doctor_update_profile(request):
    if request.method == 'POST':
        print('Post Request:', request.POST) 
        print('File Request:', request.FILES)
        form = DoctorProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = DoctorProfileForm(instance=request.user)
    return render(request, 'doctor_update_profile.html', {'form': form})