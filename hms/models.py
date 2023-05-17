from django.db import models
from django.contrib.auth.models import User
import base64
from PIL import Image
from io import BytesIO

# Create your models here.
doctor = 'Doctor'
patient = 'Patient'
admin = 'Admin'

role_choices = (
    (doctor, doctor),
    (patient, patient),
    (admin, admin),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100, choices=role_choices, null=True, blank=True)
    cnic = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Doctor(models.Model):
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="doctor_profile", null=True,
                               blank=True)
    speciality = models.CharField(max_length=100, null=True, blank=True)
    fee = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.doctor.user.get_full_name()


class Patient(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="patient_profile", null=True,
                                blank=True)
    disease_symptoms = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.patient.user.get_full_name()


class DoctorsAvailibility(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    days = models.CharField(max_length=100, null=True, blank=True)
    starting_time = models.TimeField(null=True, blank=True)
    ending_time = models.TimeField(null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)


class Slots(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    slot_date = models.DateField(null=True, blank=True)
    slot_start_time = models.TimeField(null=True, blank=True)
    slot_end_time = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.slot_date.strftime('%Y-%m-%d') + " / " + self.slot_start_time.strftime(
            '%H:%M %p') + ' - ' + self.slot_end_time.strftime(
            '%H:%M %p')


class Appointment(models.Model):
    slots = models.ForeignKey(Slots, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)


class Diagnosis(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/')
    signature_data = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
