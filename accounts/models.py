from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def users(instance, filename):
    # Generate upload path based on user's username
    return f"users/{instance.username}/{filename}"

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    EMPLOYMENT_CHOICES = [
        ('Private', 'Private'),
        ('Government', 'Government'),
    ]
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    photo = models.ImageField(upload_to='users', default='default.jpeg', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    medical_degree = models.CharField(max_length=200, null=True)
    specialty = models.CharField(max_length=200, null=True)
    medical_license_number = models.CharField(max_length=200, null=True)
    years_of_experience = models.IntegerField(max_length=10, null=True)
    current_employment = models.CharField(max_length=200, choices=EMPLOYMENT_CHOICES, null=True)
    clinic_affiliation = models.CharField(max_length=200, null=True, blank=True)
    professional_certifications = models.CharField(max_length=200, null=True)


    def __str__(self):
    	return f'{self.username}'

    class Meta:
    	ordering = ['-date_created']

