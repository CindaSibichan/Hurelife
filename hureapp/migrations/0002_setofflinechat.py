# Generated by Django 5.0.6 on 2024-07-15 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0005_alter_doctor_number_alter_patient_number'),
        ('hureapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetOfflineChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_msg', models.CharField(max_length=20)),
                ('chat_fee', models.CharField(max_length=100)),
                ('doctor_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorization.doctor')),
            ],
        ),
    ]
