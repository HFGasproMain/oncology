from django.db import models
from accounts.models import User
# Create your models here.


class MedicalHistory(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    record_date = models.DateField()
    condition = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical History for {self.patient.username}"

    class Meta:
    	ordering = ('-date_created',)



class PatientQuestion(models.Model):
    STATUS_CHOICES = (
        ('unanswered', 'Unanswered'),
        ('answered', 'Answered'),
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unanswered')
    asked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question from {self.patient.username}"

    class Meta:
        ordering = ('-asked_at',)



class DoctorResponse(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(PatientQuestion, on_delete=models.CASCADE)
    response = models.TextField()
    responded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response from {self.doctor.username}"

    class Meta:
        ordering = ('-responded_at',)
