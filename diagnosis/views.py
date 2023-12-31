from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import CancerType, Symptom, Treatment, TestResult, Patients, PatientDiagnosis
from .utils import calculate_accuracy, is_doctor, is_patient
from .forms import SymptomForm, TreatmentForm, CancerTypeForm, AddSymptomForm
#import pyttsx3
from gtts import gTTS
from django.http import FileResponse
import os



# All Views@login_required
@login_required
@user_passes_test(is_patient, login_url='login')
def diagnosis(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            selected_symptoms = form.cleaned_data['symptoms']
            possible_cancer_types = CancerType.objects.filter(symptom__in=selected_symptoms)
            treatments = Treatment.objects.filter(cancer_types__in=possible_cancer_types)

            # Perform diagnosis logic based on the selected symptoms
            diagnosis_results = []
            accuracy_scores = {}
            diagnosis_report = ""

            for cancer_type in possible_cancer_types:
                matched_symptoms = cancer_type.symptoms.filter(pk__in=selected_symptoms)

                num_matched_symptoms = matched_symptoms.count()
                num_total_symptoms = cancer_type.symptoms.count()
                print(f'matched symptoms = {num_matched_symptoms} vs total_symptoms {num_total_symptoms}')

                if num_total_symptoms > 0:
                    accuracy_scores[cancer_type] = (num_matched_symptoms / num_total_symptoms) * 100
                else:
                    accuracy_scores[cancer_type] = 0

                # Generate the diagnosis report
                diagnosis_report += f"Cancer Type: {cancer_type.name}\n"
                diagnosis_report += f"Accuracy Score: {accuracy_scores[cancer_type]}\n"
                diagnosis_report += "Matched Symptoms:\n"
                for symptom in matched_symptoms:
                    diagnosis_report += f"- {symptom.name}\n"
                diagnosis_report += "\n"

                diagnosis_results.append({
                    'cancer_type': cancer_type,
                    'matched_symptoms': matched_symptoms,
                    'accuracy_score': accuracy_scores[cancer_type],
                })



            diagnosis_results.sort(key=lambda x: x['accuracy_score'], reverse=True)
            top_diagnosis = diagnosis_results[0] if diagnosis_results else None
            print(f'Top Diagnosis => {top_diagnosis}')

            # Create a dictionary to store unique diagnoses
            unique_diagnoses = []

            for diagnosis_result in diagnosis_results:
                cancer_type = diagnosis_result['cancer_type']
                accuracy_score = diagnosis_result['accuracy_score']

                # Check if the diagnosis is already in the unique diagnoses list
                if not any(d['cancer_type'] == cancer_type for d in unique_diagnoses):
                    unique_diagnoses.append({
                        'cancer_type': cancer_type,
                        'accuracy_score': accuracy_score,
                    })

            
            accuracy = top_diagnosis['accuracy_score']
            print(f'accuracy to be saved => {accuracy}')
            stage = 0  # Initialize the stage

            if accuracy >= 75:
                stage = 4
            elif accuracy >= 50:
                stage = 3
            elif accuracy >= 25:
                stage = 2
            else:
                stage = 1


            # Save the diagnosis information to the database
            diagnosis = PatientDiagnosis(accuracy=top_diagnosis['accuracy_score'], patient=request.user, 
                cancer_type=top_diagnosis['cancer_type'].name, stage=stage)
            diagnosis.save()
            print(f'Diagnosis for {request.user} is {diagnosis}')

            # Test Result
            test_result = TestResult.objects.create(
                name=top_diagnosis['cancer_type'].name,
                accuracy=top_diagnosis['accuracy_score'],
                diagnosis_report=diagnosis_report,
                patient=request.user
            )
            test_result.symptoms.set(selected_symptoms)
            test_result.save()

            ctx = {
                'selected_symptoms': selected_symptoms,
                'diagnosis_results': unique_diagnoses,
                'top_diagnosis': top_diagnosis,
                'treatments': treatments,
                'test_result':test_result
            }
            return render(request, 'diagnosis.html', ctx)
    else:
        form = SymptomForm()
    return render(request, 'enter_symptoms.html', {'form': form})


@login_required
@user_passes_test(is_patient, login_url='login')
def test_results(request):
    test_results = TestResult.objects.filter(patient=request.user)
    return render(request, 'test_results.html', {'test_results': test_results})


# def read_diagnosis(request, pk):
#     test_result = get_object_or_404(TestResult, id=pk)
#     # Access the diagnosis and convert it to speech
#     diagnosis = test_result.diagnosis_report
#     print(f'Diag: {diagnosis}')
#     engine = pyttsx3.init()
#     print(f'engine here => {engine}')
#     engine.save_to_file(diagnosis, 'diagnosis.mp3')
#     engine.runAndWait()

#     # Return the MP3 file as the response
#     with open('diagnosis.mp3', 'rb') as file:
#         response = HttpResponse(file.read(), content_type='audio/mpeg')
#         response['Content-Disposition'] = 'attachment; filename="diagnosis.mp3"'
#         return response


@login_required
@user_passes_test(is_patient, login_url='login')
def read_diagnosis(request, pk):
    test_result = TestResult.objects.get(id=pk)
    diagnosis = test_result.diagnosis_report
    
    # Generate the speech using gTTS
    tts = gTTS(text=diagnosis, lang='en')
    tts.save('diagnosis.mp3')
    
    # Read the MP3 file as bytes
    with open('diagnosis.mp3', 'rb') as file:
        mp3_data = file.read()
    
    # Delete the temporary MP3 file
    #os.remove('diagnosis.mp3')
    
    # Return the MP3 file as the response
    response = HttpResponse(mp3_data, content_type='audio/mpeg')
    print(f'response ooo => {response}')
    response['Content-Disposition'] = 'attachment; filename="diagnosis.mp3"'
    return response


@login_required
def cancer_types(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        cancer_type = CancerType.objects.create(name=name, user=user)
        # Handle other form data or validations
        return redirect('cancer_types')
    else:
        cancer_types = CancerType.objects.filter(user=user)
        return render(request, 'cancer_types.html', {'cancer_types': cancer_types})


@login_required
def symptoms(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        symptom = Symptom.objects.create(name=name, user=user)
        # Handle other form data or validations
        return redirect('symptoms')
    else:
        symptoms = Symptom.objects.filter(user=user)
        return render(request, 'symptoms.html', {'symptoms': symptoms})


@login_required
def treatments(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        treatment = Treatment.objects.create(name=name, user=user)
        # Handle other form data or validations
        return redirect('treatments')
    else:
        treatments = Treatment.objects.filter(user=user)
        return render(request, 'treatments.html', {'treatments': treatments})


@login_required
def patients(request):
    user = request.user
    patients = Patients.objects.filter(user=user)
    return render(request, 'patients.html', {'patients': patients})


@login_required
@user_passes_test(is_doctor, login_url='login')
def add_symptom(request):
    if request.method == 'POST':
        form = AddSymptomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = AddSymptomForm()
    
    return render(request, 'add_symptom.html', {'form': form})


@login_required
@user_passes_test(is_doctor, login_url='login')
def add_treatment(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard') 
    else:
        form = TreatmentForm()
    
    return render(request, 'add_treatment.html', {'form': form})



@login_required
@user_passes_test(is_doctor, login_url='login')
def add_cancer_type(request):
    if request.method == 'POST':
        form = CancerTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard') 
    else:
        form = CancerTypeForm()
    
    return render(request, 'add_cancer_type.html', {'form': form})


def provide_recommendation(request, diagnosis_id):
    diagnosis = get_object_or_404(PatientDiagnosis, id=diagnosis_id)

    if request.method == 'POST':
        recommendation = request.POST.get('recommendation')
        diagnosis.recommendation = recommendation
        diagnosis.save()
        return redirect('doctor_dashboard')

    context = {
        'diagnosis': diagnosis,
    }
    return render(request, 'provide_recommendation.html', context)
