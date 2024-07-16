from rest_framework import serializers
from .models import *
import phonenumbers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.models import AnonymousUser
# Doctor registration serializer
class DoctorRegistrationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Doctor
        fields = ['fname', 'lname', 'number', 'dob', 'fees', 'specialization' ,'country_code','gender', 'address','experience','image']


class DoctorOTPVerifySerializer(serializers.Serializer):
    number = serializers.CharField()
    otp = serializers.CharField(max_length=6) 



# Doctor login serializer
class DoctorLoginSerializer(serializers.Serializer):
    number = serializers.CharField()





# Patient serializer
class PatientRegistrationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Patient
        fields = ['fname', 'lname', 'number', 'dob', 'email','gender','address','country_code','image']   


class PatientOTPVerifySerializer(serializers.Serializer):
    number = serializers.CharField()
    otp = serializers.CharField(max_length=6)      

    # def validate_number(self, value):
    #     try:
    #         # Parse and validate the phone number
    #         phone_number = phonenumbers.parse(value, None)  # `None` for no specific region
    #         if not phonenumbers.is_valid_number(phone_number):
    #             raise serializers.ValidationError("Invalid phone number.")
    #         return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    #     except phonenumbers.NumberParseException:
    #         raise serializers.ValidationError("Invalid phone number format.")
    


# custom refresh token serializer
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        try:
            data = super().validate(attrs)
            access_token = data['access']

            # Decode the token to add custom claims
            token = refresh.access_token

            # Identify the user type and add it to the token
            user_id = token['user_id']
            try:
                user = Patient.objects.get(id=user_id)
                user_type = 'patient'
            except Patient.DoesNotExist:
                try:
                    user = Doctor.objects.get(id=user_id)
                    user_type = 'doctor'
                except Doctor.DoesNotExist:
                    user_type = None

            if user_type:
                token['user_type'] = user_type

            data['access'] = str(token)

            return data

        except TokenError as e:
            raise InvalidToken(e.args[0])
        