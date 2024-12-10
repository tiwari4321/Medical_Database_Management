from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ResearcherProfile)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(DiseaseDetails)