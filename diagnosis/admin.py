from django.contrib import admin
from .models import CancerType, Symptom, Treatment, Patients, TestResult

# Register your models here.
#admin.site.register(CancerType)

class TreatmentInline(admin.TabularInline):
    model = CancerType.treatments.through
    extra = 1

@admin.register(CancerType)
class CancerTypeAdmin(admin.ModelAdmin):
    inlines = [TreatmentInline]

#@admin.register()


admin.site.register(Treatment)
admin.site.register(Symptom)
admin.site.register(Patients)
admin.site.register(TestResult)