# Generated by Django 5.0.6 on 2024-07-17 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0005_alter_doctor_number_alter_patient_number'),
        ('hureapp', '0005_appointment_end_time'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='appointment',
        #     name='end_time',
        #     field=models.TimeField(blank=True, null=True),
        # ),
        migrations.CreateModel(
            name='DoctorStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=400)),
                ('photo', models.ImageField(upload_to='images/')),
                ('doctor_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorization.doctor')),
            ],
        ),
    ]
