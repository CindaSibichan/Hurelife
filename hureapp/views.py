from django.shortcuts import render
from authorization.models import *
from django.contrib.auth import authenticate
from rest_framework import status ,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from authorization.utils import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied , ValidationError
from datetime import datetime, timedelta
from rest_framework.parsers import MultiPartParser, FormParser


# view Patient profile
class PatientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request ,pk=None):
        try:
            patient = Patient.objects.get(pk=pk)
            serializer = PatientProfileSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

# # view Doctor profile               
class DoctorProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request ,pk=None):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorProfileSerializer(doctor)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Doctor  not found."}, status=status.HTTP_404_NOT_FOUND)


 # edit doctor profile     
class DoctorEditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request ,pk=None):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorProfileSerializer(doctor)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Doctor  not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request , pk=None):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorProfileSerializer(doctor ,request.data , partial = True)    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Doctor.DoesNotExist:
            return Response({"error":"Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        



# edit  patient profile
class PatientEditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request ,pk=None):
        try:
            patient = Patient.objects.get(pk=pk)
            serializer = PatientProfileSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request , pk=None):
        try:
            patient = Patient.objects.get(pk=pk)
            serializer = PatientProfileSerializer(patient ,request.data , partial = True)    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({"error":"Patient not found"}, status=status.HTTP_404_NOT_FOUND)



#  list all doctors
class ListAllDoctorsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self ,request):
        try:
            doctors = Doctor.objects.all()
            serializer = DoctorProfileSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctors not found"}, status=status.HTTP_404_NOT_FOUND)




#  list all patients
class ListAllPatientsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self ,request):
        try:
            patients = Patient.objects.all()
            serializer = PatientProfileSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctors not found"}, status=status.HTTP_404_NOT_FOUND)
        


# List doctors with specialization
class ListDoctorBySpecialize(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = ListDoctorBySpecializeSerializer

 

 #create  availability of doctors (appointment planning) 
class DoctorAvailabilityView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilityPlanSerializer

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user}")
        if not isinstance(user, Doctor) or not user.is_doctor:
            raise PermissionDenied("You do not have permission to create availability.")
        serializer.save(doctor_name=user)      


# list availability
class ListDoctorAvailability(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilityPlanSerializer  



#delete availability
class DeleteDoctorAvailability(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilityPlanSerializer 
    lookup_field = 'id' 



#  Book appointment
class BookAppointment(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = BookAppointmentSerializer


    def perform_create(self, serializer):
        patient = self.request.user    # Assuming request.user is the patient instance
        doctor = serializer.validated_data.get('doctorname')
        days = serializer.validated_data.get('day_of_week')
        time = serializer.validated_data.get('time')

        # Check if doctor is available
        if not self.is_doctor_available(doctor, days, time):
            raise ValidationError("Doctor is not available at the specified time or date ")

        # Save the appointment with isdoctor_available set to True
        serializer.save(patientname=patient, isdoctor_available=True ,  payment_status=True )

    def is_doctor_available(self, doctor, day_of_week, time):
        # Check if the doctor is available at the specified time
        try:
            availability = DoctorAvailability.objects.get(
                doctor_name=doctor,
                days=day_of_week,
                start_time__lte=time,
                end_time__gte=time
            )
            return True
        except DoctorAvailability.DoesNotExist:
            return False



    # def perform_create(self, serializer):
    #     user = self.request.user
    #     print(f"User: {user}")
    #     if not isinstance(user, Patient) or not user.is_patient:
    #         raise PermissionDenied("You do not have permission to book appointments.")
    #     serializer.save(patient_name=user)   



# appointment payment 
class AppointmentPaymentView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payments.objects.all()
    serializer_class = AppointmentPaymentSerializer  




# list appointments 
class ListAppointments(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = BookAppointmentSerializer  


# delete appointments

class DeleteAppointments(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = BookAppointmentSerializer 
    lookup_field = 'id' 

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user}")
        if not isinstance(user, Patient) or not user.is_patient:
            raise PermissionDenied("You do not have permission to delete appointments.")
        serializer.save(doctorname=user) 


# offline appointment 
class SetOfflineChatView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SetOfflineChat.objects.all()
    serializer_class = SetOfflineChatSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user}")
        if not isinstance(user, Doctor) or not user.is_doctor:
            raise PermissionDenied("You do not have permission to set offline chat")
        serializer.save(doctor_name=user)



# offline chat check
class CheckOfflineChatView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SetOfflineChat.objects.all()
    serializer_class = SetOfflineChatSerializer

    def update(self, request):
        instance = self.get_object()
        current_msg_count = int(request.data.get('current_msg_count', 0))

        if current_msg_count >= int(instance.no_of_msg):
            # Logic for payment
          
            return Response({
                "message": "Message limit reached. Please pay the chat fee to continue.",
                "chat_fee": instance.chat_fee
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        return super().update(request)



# recent appointments
class RecentAppointments(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookAppointmentSerializer

    def get_queryset(self):
        # Calculate the date 3 days ago
        recent_time_frame = timezone.now() - timedelta(days=3)

        # Filter appointments that were created or occurred in the last 3 days
        return Appointment.objects.filter( date_of_appointment__gte=recent_time_frame)


    # def get_queryset(self):
    #     # Calculate the date 3 days ago
    #     recent_time_frame = timezone.now() - timedelta(days=3)  

    #     # Determine the day of the week for the recent_time_frame
    #     recent_day_of_week = recent_time_frame.strftime('%A') 

    #     # Filter appointments that fall on the recent_day_of_week
    #     return Appointment.objects.filter(day_of_week=recent_day_of_week)


# upcoming appointments
class UpcomingAppointments(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookAppointmentSerializer

    def get_queryset(self):
        now = timezone.now().date()
        
        # Filter appointments that are scheduled after the current date
        return Appointment.objects.filter(date_of_appointment__gt=now).order_by('date_of_appointment', 'time')


    # def get_queryset(self):
    #     now = timezone.now()
        
    #     # Filter appointments that are scheduled after the current date and time
    #     return Appointment.objects.filter(
    #         day_of_week__in=self.get_upcoming_days(),time__gte=now.time()).order_by('day_of_week', 'time')

    # def get_upcoming_days(self):
    #     # This method will return a list of upcoming days based on the current day
    #     current_day = timezone.now().strftime('%A')
    #     days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
    #     current_day_index = days_of_week.index(current_day)
        
    #     # Return the list of days starting from the next day to the end of the week
    #     return days_of_week[current_day_index + 1:] + days_of_week[:current_day_index]
   


# appointment for doctors 
class UpcomingAppointmentForDoctor(generics.ListAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = BookAppointmentSerializer

        def get_queryset(self):
            doctor_id = self.kwargs['doctor_id']
            now = timezone.now()
            return Appointment.objects.filter(  doctorname_id=doctor_id,
             date_of_appointment__gt=now,time__gte=now.time()).order_by('date_of_appointment', 'time')
        
        # def get_upcoming_days(self):
        # # This method will return a list of upcoming days based on the current day
        #     current_day = timezone.now().strftime('%A')
        #     days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # # Find the index of the current day
        #     current_day_index = days_of_week.index(current_day)
        
        #     return days_of_week[current_day_index + 1:] + days_of_week[:current_day_index]
   

        #     # return Appointment.objects.filter(doctorname_id=doctor_id , day_of_week__gte=today).order_by('day_of_week', 'time')




# prescriptions Create ,list ,delete
class AddPrescriptionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user}")
        if not isinstance(user, Doctor) or not user.is_doctor:
            raise PermissionDenied("You do not have permission to create prescription.")
        serializer.save(doctor_name=user) 


class ListPrescriptionView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()




class DeletePrescriptionView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user}")
        if not isinstance(user, Doctor) or not user.is_doctor:
            raise PermissionDenied("You do not have permission to delete prescription.")
        serializer.save(doctor_name=user) 



# payment details by date 
class PaymentDetailsByDate(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payments.objects.all()
    serializer_class = AppointmentPaymentSerializer  

    def get_queryset(self):
        # Get the 'date' query parameter from URL (e.g., ?date=2024-07-17)
        date_param = self.request.query_params.get('date', None)

        if date_param:
            try:
                date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
                queryset = self.queryset.filter(paid_date=date_obj)
            except ValueError:
                queryset = Payments.objects.none()  
        else:
            queryset = self.queryset

        return queryset



# doctor status 
class CreateDoctorStatusView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    queryset = DoctorStatus.objects.all()
    serializer_class = DoctorStatusSerializer

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user}")
        if not hasattr(user, 'is_doctor') or not user.is_doctor:
            raise PermissionDenied("You do not have permission to create status.")
        doctor_name = serializer.validated_data.get('doctor_name')
        if doctor_name != user:
            raise PermissionDenied("You do not have permission to create status for another doctor.")
        serializer.save(doctor_name=user)


 # list all doctor status 
class ListDoctorStatus(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DoctorStatus.objects.all()
    serializer_class = DoctorStatusSerializer

# list own doctor status

class ListOwnDoctorStatus(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorStatusSerializer

    def get_queryset(self):
            doctor_id = self.kwargs['doctor_id']
            # now = timezone.now()
            return DoctorStatus.objects.filter(doctor_name_id=doctor_id)

# delete doctor status

class DeleteDoctorStatus(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorStatusSerializer
    queryset = DoctorStatus.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user}")
        if not isinstance(user, Doctor) or not user.is_doctor:
            raise PermissionDenied("You do not have permission to delete status.")
        serializer.save(doctor_name=user) 

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.doctor_name != user:
            raise PermissionDenied("You do not have permission to delete this status.")
        instance.delete()    










 

    