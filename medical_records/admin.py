from django.contrib import admin
from .models import MedicalHistory, PatientQuestion, DoctorResponse

# Register your models here.

admin.site.register(MedicalHistory)
admin.site.register(PatientQuestion)
admin.site.register(DoctorResponse)
