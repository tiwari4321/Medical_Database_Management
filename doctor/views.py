import math
import random
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from .forms import ResearcherProfileForm, DoctorProfileForm, PatientProfileForm, DiseaseForm
from .models import *
from .filters import DiseaseFilter, PatientFilter
from .resources import diseaseResources
from django.core.files import File
import os
import zipfile
import requests
from io import StringIO
from io import BytesIO
import datetime
from django.core.paginator import Paginator
from django.conf import settings
import openpyxl

def input_data(request):
    if request.method == "POST":
        # Collect the data from the POST request
        names = request.POST.getlist('name')
        diagonises = request.POST.getlist('diagonised')
        modalities = request.POST.getlist('modality')

        # Create a new Excel workbook
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'User Data'

        # Add headers to the Excel file
        sheet.append(['Name', 'Diagonised','Modality'])

        # Populate the Excel file with the submitted data
        for name, diag, modality in zip(names, diagonises, modalities):
            sheet.append([name, diag, modality])

        # Prepare the response to send the Excel file
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="user_data.xlsx"'
        wb.save(response)

        return response

    # Initial rows to display in the form (can be empty or predefined)
    initial_rows = [{'name': '', 'diagonised': '', 'modality': ''}]
    return render(request, 'input_form.html', {'rows': initial_rows}) 


# Create your views here.
@login_required
def researcher_profile(request):
    if(ResearcherProfile.objects.filter(researcher=request.user).exists()):
        researcher = researcher = ResearcherProfile.objects.get(researcher=User.object.get(id=request.user.id))
        context = {
         'researcher': researcher
        }
        return render(request, 'researcher/profile.html', context)
    else:
        if request.method == 'POST':
            fm = ResearcherProfileForm(request.POST,request.FILES)
            if fm.is_valid():
                instance = fm.save(commit=False)
                instance.researcher = request.user
                instance.first_name=instance.first_name.capitalize()
                instance.last_name=instance.last_name.capitalize()
                instance.organization=instance.organization.capitalize()
                
                print(instance.id)
                instance.save()
                messages.success(request, 'Your profile has been created')
                researcher = researcher = ResearcherProfile.objects.get(researcher=User.object.get(id=request.user.id))
                context = {
                'researcher': researcher
                    }

                return render(request, 'researcher/profile.html', context)
            else:
                messages.error(request, 'Please enter valid details')
                return render(request,'researcher/profile-form.html',{'form':fm})
        else:
                fm=ResearcherProfileForm()
                return render(request,'researcher/profile-form.html',{'form':fm})

@login_required
def profile(request):
    if request.user.is_doctor == True :
        return redirect('profile_doctor')
    elif request.user.is_researcher == True :
        return redirect('profile_researcher')
    else:
        print("NOT A Researcher!! and not a Doctor")
        return redirect('login')

def check_profile_created(request):
    if request.user.is_doctor == True : 
        if(DoctorProfile.objects.filter(doctor=request.user).exists()):
            return True
        else:
            return False
    else:
        if(ResearcherProfile.objects.filter(researcher=request.user).exists()):
            return True
        else:
            return False

def check_admin_verified(request):
    doctor = DoctorProfile.objects.get(doctor=User.object.get(id=request.user.id))
    if(doctor.verified_admin==True):
        return True
    else:
        return False

@login_required
def doctor_profile(request):
    if(DoctorProfile.objects.filter(doctor=request.user).exists()):
        dcotor = doctor = DoctorProfile.objects.get(doctor=User.object.get(id=request.user.id))
        context = {
         'doctor': doctor
        }
        return render(request, 'doctor/profile.html', context)
    else:
        if request.method == 'POST':
            fm = DoctorProfileForm(request.POST)
            if fm.is_valid():
                instance = fm.save(commit=False)
                instance.doctor = request.user
                instance.first_name=instance.first_name.capitalize()
                instance.last_name=instance.last_name.capitalize()
                instance.specialization=instance.specialization.capitalize()
                print(instance.id)
                instance.save()
                messages.success(request, 'Your profile has been created')
                doctor = doctor = DoctorProfile.objects.get(doctor=User.object.get(id=request.user.id))
                context = {
                'doctor': doctor
                    }

                return render(request, 'doctor/profile.html', context)
            else:
                messages.error(request, 'Please enter valid details')
                return render(request,'doctor/profile-form.html',{'form':fm})
        else:
                fm=DoctorProfileForm()
                return render(request,'doctor/profile-form.html',{'form':fm})

@login_required
def add_patient(request):
    if request.user.is_doctor == True : 
        if check_profile_created(request=request)==True:
            if check_admin_verified(request=request)==True:
                if request.method == 'POST':
                    fm = PatientProfileForm(request.POST)
                    if fm.is_valid():
                        instance = fm.save(commit=False)
                        instance.added_by = request.user
                        instance.first_name = instance.first_name.capitalize()
                        instance.last_name = instance.last_name.capitalize()
                        instance.city = instance.city.capitalize()
                        instance.hospital = instance.hospital.capitalize()
                        instance.save()
                        messages.success(request,"Patient has been added successfully")
                        return redirect('show_patient')
                    else:
                        messages.error(request,"Please enter valid details")
                        return render(request,'doctor/patient-form.html',{'form':fm})
                else:
                    fm = PatientProfileForm()
                    return render(request,'doctor/patient-form.html',{'form':fm})
            else:
                messages.error(request,"Your profile is not verified by admin yet ")
                return redirect("profile_user")
        else:
            messages.error(request,"Please first create your profile ")
            return redirect("profile_user")
            
    else:
        messages.error(request,"You are not authorized to visit that page")
        return redirect('index')

@login_required
def show_patient(request):
    if request.user.is_doctor == True :
        if check_profile_created(request=request)==True:
            if check_admin_verified(request=request)==True:
                patient = PatientProfile.objects.filter(added_by=User.object.get(id=request.user.id))
                myfilter = PatientFilter(request.GET,queryset=patient)
                patient = myfilter.qs
                paginator = Paginator(patient,6)
                page_number=request.GET.get('page')
                PatientFinal=paginator.get_page(page_number)
                context = {
                'patients': PatientFinal,
                'myfilter':myfilter
                }
                return render(request, 'doctor/patients.html', context)
            else:
                messages.error(request,"Your profile is not verified by admin yet ")
                return redirect("profile_user")
        else:
            messages.error(request,"Please first create your profile ")
            return redirect("profile_user")
    else:
        messages.error(request,"You are not authorized to visit this")
        return redirect('index')

@login_required
def show_patient_details(request, id):
    if request.user.is_doctor == True :
        patient = PatientProfile.objects.get(id=id)
        diseases = DiseaseDetails.objects.filter(patient=id)
        myfilter = DiseaseFilter(request.GET,queryset=diseases)
        diseases = myfilter.qs
        paginator = Paginator(diseases,5)
        page_number=request.GET.get('page')
        DiseaseFinal=paginator.get_page(page_number)
        context = {
        'patient': patient,
        'diseases':DiseaseFinal,
        'myfilter':myfilter
        }
        return render(request, 'doctor/patient-profile.html', context)
    else:
        messages.error(request,"You are not authorized to visit this")
        return redirect('index')

@login_required
def add_disease_patient(request, id):
    if request.user.is_doctor == True : 
        patient = PatientProfile.objects.get(id=id)
        if request.method == 'POST':
            messages.info(request,"Doctors are advised to take consent from patient before uploading data")
            fm = DiseaseForm(request.POST,request.FILES)
            # fm.patient=patient
            if fm.is_valid():
                instance = fm.save(commit=False)
                instance.patient=patient
                instance.name=instance.name.capitalize()
                instance.organ=instance.organ.capitalize()
                instance.date=datetime.date.today()
                print(instance.img)
                instance.save()
                messages.success(request,"Disease details has been added successfully")
                return redirect('show_patient')
            else:
                messages.error(request,"Please enter valid details")
                return render(request,'doctor/disease-form.html',{'form':fm,'patient':patient})
        else:
            fm = DiseaseForm()
            return render(request,'doctor/disease-form.html',{'form':fm,'patient':patient})
    else:
        messages.error(request,"You are not authorized to visit that page")
        return redirect('index')

@login_required
def show_disease(request):
    if check_profile_created(request=request)==True:
        diseases = DiseaseDetails.objects.all()
        myfilter = DiseaseFilter(request.GET,queryset=diseases)
        diseases=myfilter.qs
        print(request)
        if request.method == 'POST' :
            # File f
            data = request.POST
            print(data)
            action = data.get("follow")
            print(action)
            if action == "follow":
                print("hello")
                dataset = diseaseResources().export(diseases).xls
                response = HttpResponse(dataset,content_type='xls')
                response['Content-Disposition'] = 'attachment; filename="disease.xls"'
                return response
            filenames= []
            for disease in diseases:
                filenames.append(disease.img.path)
            
            zip_subdir = "Images"
            zip_filename = "%s.zip" % zip_subdir

            # Open StringIO to grab in-memory ZIP contents
            s =  BytesIO()

            # The zip compressor
            zf = zipfile.ZipFile(s, "w")

            for fpath in filenames:
                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                print(fdir)
                # xpath = os.path.abspath(fpath)
                # print(xpath)
                # zip_path = os.path.join(zip_subdir, fname)
                zip_path = os.path.join(fdir, fname)


                # Add file, at correct path
                # zf.write(fpath, zip_path)
                zf.write(fpath, zip_path)


            # Must close zip for all contents to be written
            zf.close()

            # Grab ZIP file from in-memory, make response with correct MIME-type
            resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
            # ..and correct content-disposition
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

            return resp
        else:
            paginator = Paginator(diseases,5)
            page_number=request.GET.get('page')
            DiseaseFinal=paginator.get_page(page_number)
            context = {
            'diseases': DiseaseFinal,
            'myfilter': myfilter
            }
            return render(request, 'doctor/diseases.html', context)
    else:
        messages.error(request,"Please first create your profile ")
        return redirect("profile_user")



def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


api_key = settings.API_KEY
def otp_verify_send(request):
    if request.user.is_doctor:
        doctor = DoctorProfile.objects.get(doctor=User.object.get(id=request.user.id))
        otp=generateOTP()
        doctor.otp = otp
        
        url = f'https://2factor.in/API/V1/{api_key}/SMS/+91{doctor.phone}/{otp}/'
        requests.get(url)
        doctor.save()
        messages.info(request,"OTP has been send to your registered number")
        return render(request,'account/otpverify.html')
    else:
        researcher = ResearcherProfile.objects.get(researcher=User.object.get(id=request.user.id))
        otp=generateOTP()
        print("A" + otp)
        researcher.otp=otp
        researcher.save()
        
        url = f'https://2factor.in/API/V1/{api_key}/SMS/+91{researcher.phone}/{otp}/OTP1'
        requests.get(url)
        messages.info(request,"OTP has been send to your registered number")
        return render(request,'account/otpverify.html')
        
def verify_otp(request):
    if request.method=='POST':
        otp = request.POST['otp']
        if request.user.is_doctor==True:
            doctor = DoctorProfile.objects.get(doctor=User.object.get(id=request.user.id))
            if(doctor.otp==otp):
                messages.success(request,"Your phone number is verified")
                doctor.verified_phone=True
                doctor.save()
                return redirect('profile_user')
            else:
                messages.error(request,"Incorrect otp")
                return render(request,'account/otpverify.html')
        else:
            researcher = ResearcherProfile.objects.get(researcher=User.object.get(id=request.user.id))
            if(researcher.otp==otp):
                messages.success(request,"Your phone number is verified")
                researcher.verified_phone=True
                researcher.save()
                return redirect('profile_user')
            else:
                messages.error(request,"Incorrect otp")
                return render(request,'account/otpverify.html')

    else:
        return redirect('otp_verify')

