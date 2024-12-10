"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('signup_researcher',views.ResearcherSignup,name='signup_researcher'),
    path('signup_doctor',views.DoctorSignup,name='signup_doctor'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(), name='activate'),
    path('login',views.login_view,name='login'),
    path('logout', views.logout_view,name='logout'),
    path('request-reset-email',views.RequestResetEmail.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(), name='set-new-password'),
    path('user/',include('doctor.urls') ),
    path('about/',views.about,name='about'),
    path('Physiological_data/', views.Physiological_data, name='physiological_data'),
    
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

