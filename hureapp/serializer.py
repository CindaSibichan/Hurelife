from rest_framework import serializers
from authorization.models import *
from .models import *

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['fname', 'lname', 'number', 'dob', 'email','gender','address','country_code','image' ,'otp','is_verified']

        read_only_fields = ['otp', 'is_verified'] 


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields =  [
            'fname', 'lname', 'number', 'dob', 'fees', 'specialization',
            'otp', 'is_verified', 'image', 'gender', 'address',
            'country_code', 'experience', 'is_active'
        ]
        read_only_fields = ['otp', 'is_verified' , 'is_active'] 


#list doctors with their specilaization
class ListDoctorBySpecializeSerializer(serializers.Serializer):
    fname = serializers.CharField()
    lname = serializers.CharField()
    specialization = serializers.CharField()



# doctor appointment planning
class DoctorAvailabilityPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'


 # book apointment serializer
class  BookAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Appointment
        fields = '__all__'




 # appointment payment serializer
class AppointmentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class SetOfflineChatSerializer(serializers.ModelSerializer):
    class Meta :
        model = SetOfflineChat
        fields = '__all__'





# prescription serializer 
class PrescriptionSerializer(serializers.ModelSerializer):
    report = serializers.ImageField(required = False)
    prescription = serializers.ImageField(required = False)
    class Meta:
        model = Prescription
        fields = ['doctor_name','patient_name','notes','report','prescription','msgtype']      

# doctor status serializer

class DoctorStatusSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()
    class Meta:
        model = DoctorStatus
        fields =['doctor_name' , 'message' , 'photo']
