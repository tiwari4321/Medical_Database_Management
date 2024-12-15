from django import forms

from .models import *

class ResearcherProfileForm(forms.ModelForm):

    class Meta:
        model = ResearcherProfile

        fields = ['first_name', 'last_name', 'gender', 'phone', 'dob','country','organization','id_image']

class DoctorProfileForm(forms.ModelForm):

    class Meta:
        model = DoctorProfile

        fields = ['first_name', 'last_name', 'gender', 'phone', 'dob','license_key','specialization']

class PatientProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfile

        fields = ['first_name', 'last_name', 'gender', 'phone', 'dob','hospital','city','blood_group']

class DiseaseForm(forms.ModelForm):

    class Meta:
        model = DiseaseDetails
        fields = ['name', 'modality', 'diagonised', 'img','organ','age','systolic_blood_pressure','diastolic_blood_pressure','cholesterol_level','sugar_level','blood_oxygen_saturation','heart_rate','smoking','alcohol','physically_inactive','stress','weight','height','gender','electrolyte_level','chronic_kidney']
        