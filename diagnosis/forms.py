from django import forms
from .models import Symptom, Treatment, CancerType
from django.contrib.auth.decorators import login_required

class SymptomForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class AddSymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ('name',)


class DiagnosisForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(queryset=Symptom.objects.all(), widget=forms.CheckboxSelectMultiple)


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ('name',)


class CancerTypeForm(forms.ModelForm):
    class Meta:
        model = CancerType
        fields = ('name', 'treatments', 'symptoms')
        widgets = {
            'treatments': forms.CheckboxSelectMultiple,
            'symptoms': forms.CheckboxSelectMultiple,
        }