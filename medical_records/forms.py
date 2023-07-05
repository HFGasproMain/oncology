from django import forms
from .models import MedicalHistory, PatientQuestion, DoctorResponse

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['record_date', 'condition', 'description']


class PatientQuestionForm(forms.ModelForm):
    class Meta:
        model = PatientQuestion
        fields = ['question']



class DoctorResponseForm(forms.ModelForm):
    class Meta:
        model = DoctorResponse
        fields = ['response']


class RespondToQuestionForm(forms.Form):
    response = forms.CharField(label='Response', widget=forms.Textarea(attrs={'rows': 4}))