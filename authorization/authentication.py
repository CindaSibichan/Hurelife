from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from .models import *



class CustomJWTAuthentication(JWTAuthentication):
    user_id_field = 'user_id'
    user_type_field = 'user_type'

    def get_user(self, validated_token):
        try:
            user_id = validated_token[self.user_id_field]
            user_type = validated_token[self.user_type_field]
        except KeyError:
            raise exceptions.AuthenticationFailed('Token contained no recognizable user identification')

        if user_type == 'patient':
            try:
                user = Patient.objects.get(id=user_id)
            except Patient.DoesNotExist:
                raise exceptions.AuthenticationFailed('No patient matching this token was found.')
        elif user_type == 'doctor':
            try:
                user = Doctor.objects.get(id=user_id)
            except Doctor.DoesNotExist:
                raise exceptions.AuthenticationFailed('No doctor matching this token was found.')
        else:
            raise exceptions.AuthenticationFailed('Invalid user type.')

        if not user.is_verified:
            raise exceptions.AuthenticationFailed('User is not verified.')

        return user

# class CustomJWTAuthentication(JWTAuthentication):
#     user_id_field = 'user_id' 

#     def get_user(self, validated_token):
#         try:
#             user_id = validated_token[self.user_id_field]
#         except KeyError:
#             raise exceptions.AuthenticationFailed('Token contained no recognizable user identification')

#         try:
#             user = Patient.objects.get(id=user_id)
#         except Patient.DoesNotExist:
#             try:
#                 user = Doctor.objects.get(id=user_id)
#             except Doctor.DoesNotExist:
#                 raise exceptions.AuthenticationFailed('No user matching this token was found.')

#         if not user.is_verified:
#             raise exceptions.AuthenticationFailed('User is not verified.')

#         return user