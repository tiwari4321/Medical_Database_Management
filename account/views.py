# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
from .models import User as Accounts

# Create your views here.
def index(request):
    return render(request,'account/home.html')

def ResearcherSignup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confpassword = request.POST['confpassword']


        if (Accounts.object.filter(email=request.POST['email']).exists()):
            messages.error(request,'User with this email already exists')
            return render(request,'account/signup_researcher.html')



        elif password != confpassword:
            messages.error(request,'Password dont match')
            return render(request,'account/signup_researcher.html')


        else:
            user = Accounts.object.create_user(email=email, password = password)
            user.is_researcher=True
            user.is_doctor=False                                                                
            user.is_active=True
            user.save()
            current_site=get_current_site(request)
            email_subject='Activate your account',
            message=render_to_string('account/activate_account.html',
            {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),


            }

            )
            email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
            )
            email_message.send()



            messages.success(request,'Account created ,activate your account !! Mail has been sent to the registered email')
            return redirect('login')
    else:
        return render(request,'account/signup_researcher.html')


def DoctorSignup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confpassword = request.POST['confpassword']


        if (Accounts.object.filter(email=request.POST['email']).exists()):
            messages.error(request,'User with this email already exists')
            return render(request,'account/signup_doctor.html')



        elif password != confpassword:
            messages.error(request,'Password dont match')
            return render(request,'account/signup_doctor.html')


        else:
            user = Accounts.object.create_user(email=email, password = password)
            user.is_researcher=False
            user.is_doctor=True
            user.is_active=False
            user.save()
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            print(user.pk)
            current_site=get_current_site(request)
            email_subject='Activate your account',
            message=render_to_string('account/activate_account.html',
            {
                'user':user,
                'domain':current_site.domain,
                'uid':uid,
                'token':generate_token.make_token(user),


            }

            )
            email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
            )
            email_message.send()



            messages.success(request,'Account created ,activate your account !! Mail has been sent to the registered email')
            return redirect('login')
    else:
        return render(request,'account/signup_doctor.html')




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_researcher:
                return redirect('profile_researcher')

            if request.user.is_doctor:
                return redirect('profile_doctor')



        else:
            messages.error(request,'Enter valid email and password')
            return render(request,'account/login.html')

    else:
        return render(request,'account/login.html')

def logout_view(request):

    logout(request)
    return redirect('login')

def about(request):
    return render(request,'account/about.html')

def Physiological_data(request):
    return render(request, 'doctor/physiological_data.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=Accounts.object.get(pk=uid)
        except Exception as identifier:
            print(Exception)
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,'Activated the account')
            return redirect('login')
        else:
            messages.info(request,'Activation failed')
            return render(request,'account/activate_failed.html', status=401)


class RequestResetEmail(View):
    def get(self,request):
        return render(request,'account/request-reset-email.html')

    def post(self,request):
        email=request.POST['email']



        user=Accounts.object.filter(email=email)

        if user.exists():
            current_site=get_current_site(request)
            email_subject='[Reset your password]',
            message=render_to_string('account/reset-user-password.html',
            {

                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0]),


            }

            )
            email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
            )
            email_message.send()


            messages.success(request,'we have sent you password reset link')
            return render(request,'account/request-reset-email.html')
        else:
            messages.error(request,'No such user exist')
            return render(request,'account/request-reset-email.html')



class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        return render(request,'account/set-new-password.html',context)
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }

        password = request.POST['password']
        confpassword = request.POST['confpassword']
        if password != confpassword:
            messages.error(request,'Password dont match')
            return render(request,'account/set-new-password.html',context)
        try:
            user_id= force_str(urlsafe_base64_decode(uidb64))
            user=Accounts.object.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password changed')
            return redirect('login')


        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,'Something went wrong')
            return render(request,'account/set-new-password.html',context)



        return render(request,'account/set-new-password.html',context)