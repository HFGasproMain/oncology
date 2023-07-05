from django.urls import path
from .views import index, home, doctor_registration, patient_registration, user_login, doctor_dashboard, \
    patient_dashboard, about_us, update_profile
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', home, name='home'),
	path('register/doctor/', doctor_registration, name='doctor_registration'),
    path('register/patient/', patient_registration, name='patient_registration'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('about-us/', about_us, name='about_us'),
    path('profile/update/', update_profile, name='update_profile'),
]
