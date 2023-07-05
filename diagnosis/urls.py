from django.urls import path
from .views import diagnosis, read_diagnosis, test_results, add_symptom, add_cancer_type, add_treatment

urlpatterns = [
	path('diagnosis/', diagnosis, name='start-diagnosis'),
	path('results/', test_results, name='test-results'),
	path('results/<int:pk>/read/', read_diagnosis, name='read_diagnosis'),
	path('add-symptom/', add_symptom, name='add_symptom'),
	path('add-treatment/', add_treatment, name='add_treatment'),
    path('add-cancer-type/', add_cancer_type, name='add_cancer_type'),
]