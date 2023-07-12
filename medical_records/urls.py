from django.urls import path
from .views import add_medical_history, ask_question, view_medical_history, respond_to_question, \
	view_patient_questions, patient_questions, view_response, view_patient_diagnosis

urlpatterns = [
    # other URL patterns
    path('add-medical-history/', add_medical_history, name='add_medical_history'),
    path('ask-question/', ask_question, name='ask_question'),
    path('view-medical-history/', view_medical_history, name='view_medical_history'),
    path('view-patient-questions/', view_patient_questions, name='patient_questions'),
    path('view-patient-diagnosis/', view_patient_diagnosis, name='patient_diagnosis'),
    path('my-questions/', patient_questions, name='my_questions'),
    path('respond-to-question/<int:question_id>/', respond_to_question, name='respond_to_question'),
    path('view_response/<int:question_id>/', view_response, name='view_response'),
]
