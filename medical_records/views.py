from django.shortcuts import render, redirect
from .forms import MedicalHistoryForm, PatientQuestionForm, RespondToQuestionForm
from django.contrib.auth.decorators import login_required, user_passes_test
from diagnosis.utils import is_patient, is_doctor
from .models import MedicalHistory, PatientQuestion, DoctorResponse

# Create your views here.

@login_required
@user_passes_test(is_patient, login_url='login')
def add_medical_history(request):
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient = request.user
            medical_history.save()
            return redirect('patient_dashboard')
    else:
        form = MedicalHistoryForm()
    return render(request, 'add_medical_history.html', {'form': form})



@login_required
@user_passes_test(is_patient, login_url='login')
def ask_question(request):
    if request.method == 'POST':
        form = PatientQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.patient = request.user
            question.save()
            print('Question asked successfully!')
            return redirect('my_questions')
    else:
        form = PatientQuestionForm()
    return render(request, 'ask_question.html', {'form': form})



@login_required
@user_passes_test(is_doctor, login_url='login')
def view_medical_history(request):
    if request.user.user_type == 'doctor':
        medical_history = MedicalHistory.objects.all()
        return render(request, 'view_medical_history.html', {'medical_history': medical_history})



@login_required
@user_passes_test(is_patient, login_url='login')
def my_medical_history(request):
    if request.user.user_type == 'doctor':
        my_medical_history = MedicalHistory.objects.filter(patient=request.user)
        return render(request, 'my_medical_history.html', {'my_medical_history': my_medical_history})


@login_required
@user_passes_test(is_doctor, login_url='login')
def view_patient_questions(request):
    questions = PatientQuestion.objects.all()
    return render(request, 'view_patient_questions.html', {'questions': questions})


@login_required
@user_passes_test(is_patient, login_url='login')
def patient_questions(request):
    questions = PatientQuestion.objects.filter(patient=request.user)
    return render(request, 'my_questions.html', {'questions': questions})



@login_required
@user_passes_test(is_doctor, login_url='login')
def respond_to_question(request, question_id):
    question = PatientQuestion.objects.get(pk=question_id)
    if request.method == 'POST':
        form = RespondToQuestionForm(request.POST)
        if form.is_valid():
            response_text = form.cleaned_data['response']
            doctor = request.user
            response = DoctorResponse.objects.create(doctor=doctor, question=question, response=response_text)
            question.status = 'answered'
            question.save()
            #response.save()
            print('Successful!')
            return redirect('doctor_dashboard')
    else:
        form = RespondToQuestionForm()
    return render(request, 'respond_to_question.html', {'form': form, 'question': question})


@login_required
@user_passes_test(is_patient, login_url='login')
def view_response(request, question_id):
    question = PatientQuestion.objects.get(pk=question_id)
    response = DoctorResponse.objects.filter(question=question).first()
    return render(request, 'view_response.html', {'question': question, 'response': response})
