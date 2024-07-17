from django.db import models
from authorization.models import *
from django.utils import timezone
from datetime import date
from datetime import datetime ,timedelta

# Create your models here.

class DoctorAvailability(models.Model):
    DAYS_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    days = models.CharField(max_length=20 , choices= DAYS_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.doctor_name)
    


class Appointment(models.Model):
    APPOINTMENT_TYPES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
    ]

    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    patientname = models.ForeignKey(Patient , on_delete=models.CASCADE)
    doctorname = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20 , choices= DAYS_OF_WEEK)
   
    time = models.TimeField()
    appointment_type = models.CharField(max_length=10,choices=APPOINTMENT_TYPES)
    payment_status = models.BooleanField(default=False)
    isdoctor_available = models.BooleanField(default=False)
    payment_amount = models.CharField(max_length=100 ,default=0)
    payment_date = models.DateField()
    date_of_appointment = models.DateField(default=date.today())
    end_time = models.TimeField(null=True , blank=True)


    def save(self, *args, **kwargs):
        if self.appointment_type == 'ONLINE' and self.time:
            start_datetime = timezone.datetime.combine(self.date_of_appointment, self.time)
            end_datetime = start_datetime + timedelta(minutes=30)
            self.end_time = end_datetime.time()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.patientname)


class Payments(models.Model):
    patient_name = models.ForeignKey(Patient , on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    paid_amount = models.CharField(max_length=200)
    paid_date = models.DateField()
    payment_status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.patient_name)


class SetOfflineChat(models.Model):
    doctor_name = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    no_of_msg = models.CharField(max_length=20)
    chat_fee = models.CharField(max_length=100)

    def __str__(self):
        return str(self. doctor_name)
    

    
class Prescription(models.Model):
    doctor_name = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    patient_name = models.ForeignKey(Patient,on_delete=models.CASCADE)
    notes = models.CharField(max_length=300)
    report = models.ImageField(null=True,blank=True, upload_to='images/')
    prescription = models.ImageField(null=True,blank=True, upload_to='images/')
    msgtype = models.CharField(max_length=100)

    def __str__(self):
        return str(self. doctor_name)



class DoctorStatus(models.Model):
    doctor_name = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    message = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='images/')


    def __str__(self):
        return str(self. doctor_name)
  