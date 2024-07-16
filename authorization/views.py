from django.shortcuts import render
from .serializers import *
from rest_framework import generics
import random
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import *
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import phonenumbers
import jwt
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
import re
from rest_framework import exceptions

# Create your views here.



# Doctor registration
class DoctorRegistrationView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            otp = send_otp_num(doctor.number)
            doctor.otp = str(otp)
            doctor.save()
            return Response({"message": "Doctor registered. OTP sent to your mobile number"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
class DoctorOTPVerificationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = DoctorOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            otp = str(serializer.validated_data['otp'])
            try:
                doctor = Doctor.objects.get(number=number, otp=otp)
                doctor.is_verified = True
                doctor.is_doctor = True
                doctor.otp = None  
                doctor.save()
                
                return Response({"message": "Doctor Verified successfully."}, status=status.HTTP_200_OK)
            except Doctor.DoesNotExist:
                return Response({"error": "Invalid OTP or number."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Doctor Login
class DoctorLoginView(APIView):
    permission_classes = [AllowAny]
    def post( self , request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            try:
                doctor = Doctor.objects.filter(number__in=[number, f"+91 {number}"]).first()
                if doctor and doctor.is_active and doctor.is_verified and doctor.is_doctor:
                    otp = send_otp_num(doctor.number)
                    doctor.otp = str(otp)
                    doctor.save()
                    return Response({"message": "OTP sent to your number."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Doctor not verified or not activated."}, status=status.HTTP_400_BAD_REQUEST)
            except Doctor.DoesNotExist:
                return Response({"error": "Doctor not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                     
class LoginOTPVerifyView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = DoctorOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            otp = serializer.validated_data['otp']
            print(f"Number received: {number}")
            print(f"OTP received: {otp}")
            try:
                doctor = Doctor.objects.filter(number__in=[number, f"+91 {number}"]).first()
                if doctor:
                    print(f"Doctor found: {doctor.id} - {doctor.number}")
                else:
                    print(f"No doctor found with number: {number}")
                # doctor = Doctor.objects.get(number=number, otp=otp)
                if doctor and doctor.is_verified and doctor.is_active and doctor.is_doctor:
                    refresh = RefreshToken.for_user(doctor)
                    refresh['user_type'] = 'doctor'
                    doctor.otp = None  # Clear OTP after successful login
                    doctor.save()
                    return Response({
                       
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid OTP or doctor not verified."}, status=status.HTTP_400_BAD_REQUEST)
            except Doctor.DoesNotExist:
                print(f"Doctor not found for number: {number}")
                return Response({"error": "Invalid OTP or number."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




                    
# Patient regsitration view 
class PatientRegistrationView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            otp = send_otp_num(patient.number)
            patient.otp = str(otp)
            patient.save()
            return Response({"message": "Patient registered. OTP sent to your mobile number"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 




class PatientOTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            otp = str(serializer.validated_data['otp'])
            print(f"Number: {number}, OTP: {otp}")
            try:
                # patient = Patient.objects.filter(number__in=[number, f"+91 {number}"]).first()
                patient = Patient.objects.filter(number__in=[number, f"+91 {number}" , f"+91{number}"]).first()
                print(f"Patient found: {patient}")
                refresh = RefreshToken.for_user(patient)
                refresh['user_type'] = 'patient'
                patient.is_verified = True
                patient.is_patient = True
                patient.otp = None  
                patient.save()
                return Response({
                    "message": "Patient Verified successfully.",
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except Patient.DoesNotExist:
                return Response({"error": "Invalid OTP or number."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class PatientOTPVerificationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = PatientOTPVerifySerializer(data=request.data)
#         if serializer.is_valid():
#             number = serializer.validated_data['number']
#             otp = str(serializer.validated_data['otp'])
#             try:
#                 # patient = Patient.objects.get(number=number, otp=otp)
#                 patient = Patient.objects.filter(number__in=[number, f"+91 {number}" , f"+91{number}"]).first()
#                 # patient = Patient.objects.filter(
#                 #     number=number
#                 # ).union(
#                 #     Patient.objects.filter(number__iexact=f"+{number}"),  # Matches with '+' and country code
#                 #     Patient.objects.filter(number__iexact=f"+91 {number}")  # Matches with specific country code
#                 # ).first()
#                 refresh = RefreshToken.for_user(patient)
#                 patient.is_verified = True
#                 patient.otp = None  
#                 patient.save()
#                 return Response({
#                     "message": "Patient Verified successfully.",
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }, status=status.HTTP_200_OK )
               
#             except Patient.DoesNotExist:
#                 return Response({"error": "Invalid OTP or number."}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#generate access token using refresh token
class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomTokenRefreshSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





