from django.urls import path
from .views import diagnosis, read_diagnosis, test_results

urlpatterns = [
	path('diagnosis/', diagnosis, name='start-diagnosis'),
	path('results/', test_results, name='test-results'),
	path('results/<int:pk>/read/', read_diagnosis, name='read_diagnosis'),
]