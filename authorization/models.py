from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField



# Create your models here.

class Patient(models.Model):
    fname = models.CharField(max_length=200,null=False,blank=False)
    lname = models.CharField(max_length=200,null=False,blank=False)
    number = models.CharField(max_length=20,null=False,blank=False,unique=True)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=False,blank=False , upload_to='images/')
    GENDER_CHOICES = [

        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(max_length=300,null=False,blank=False )
    country_code = models.IntegerField(null=False, blank=False)
    is_patient = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True  # 

    def __str__(self):
        return self.fname

    

class Doctor(models.Model):
    fname = models.CharField(max_length=200,null=False,blank=False)
    lname = models.CharField(max_length=200,null=False,blank=False)
    number = models.CharField(max_length=20,null=False,blank=False,unique=True)
    dob = models.DateField()
    fees = models.IntegerField()
    specialization = models.CharField(max_length=200 , null=False , blank=False)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=False,blank=False ,  upload_to='images/' )
    GENDER_CHOICES = [

        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(max_length=300,null=False,blank=False)
    country_code = models.IntegerField(null=False, blank=False)
    experience = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True  

    def __str__(self):
        return self.fname
    



