from django.db import models
from accounts.models import User

# Create your models here.
class CancerType(models.Model):
    name = models.CharField(max_length=100)
    treatments = models.ManyToManyField('Treatment')
    symptoms = models.ManyToManyField('Symptom', related_name='symptoms')

    def __str__(self):
    	return self.name

    class Meta:
        ordering = ['id']

class Symptom(models.Model):
    name = models.CharField(max_length=100)
    cancer_types = models.ManyToManyField(CancerType)

    def __str__(self):
    	return self.name

    class Meta:
        ordering = ['-id']

class Treatment(models.Model):
    name = models.CharField(max_length=100)
    cancer_types = models.ManyToManyField(CancerType)

    def __str__(self):
    	return self.name


class Patients(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	symptoms = models.ManyToManyField(Symptom)

	def __str__(self):
		return '{},{}'.format(self.user, self.test_results)


class PatientDiagnosis(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_diagnosis')
    accuracy = models.FloatField()
    cancer_type = models.CharField(max_length=100)
    stage = models.IntegerField()
    recommendation = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis for {self.patient} - CancerType {self.cancer_type} at Stage {self.stage}"

    class Meta:
        ordering = ('-date_created',)



class TestResult(models.Model):
    name = models.CharField(max_length=100)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_result', null=True)
    cancer_types = models.ManyToManyField(CancerType)
    symptoms = models.ManyToManyField(Symptom)
    accuracy = models.FloatField(default=0.0)
    diagnosis_report = models.TextField(null=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-saved_at']