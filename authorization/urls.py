from django.urls import path,include
from . views import *
 

urlpatterns = [

# Doctor
    path('docregister/' , DoctorRegistrationView.as_view() , name='doctor-register' ),
    path('otp-verify/',DoctorOTPVerificationView.as_view(),name='doctor-verify'),
    path('doctor-login/',DoctorLoginView.as_view() ,name="doctor-login" ),
    path('doclogin-verify/',LoginOTPVerifyView.as_view(), name="doclogin-verify"),
# Patient
    path('pregister/' , PatientRegistrationView.as_view(), name='patient-register' ),
    path('pverify-otp/',PatientOTPVerificationView.as_view(),name='patient-verify'),



] 
 