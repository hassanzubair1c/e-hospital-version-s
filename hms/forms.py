from django import forms
from django.forms import PasswordInput, TextInput
from django.forms.widgets import CheckboxInput, SelectDateWidget, DateInput

import hms.models
from .models import *
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    cnic = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)
    confirm_password = forms.CharField(max_length=100, required=True)


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'type': 'password', 'autocomplete': 'nope'}))


class UserEditForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    cnic = forms.CharField(max_length=100, required=True)


class DoctorForm(forms.ModelForm):
    speciality = forms.ChoiceField(choices=[
        ('dentist', 'Dentist'),
        ('dermatologist', 'Dermatologist'),
        ('hematologist', 'Hematologist'),
        ('nephrologist', 'Nephrologist'),
        ('neurologist', 'Neurologist'),
    ])

    class Meta:
        model = Doctor
        fields = ['doctor', 'speciality', 'fee']

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = UserProfile.objects.filter(role=hms.models.doctor)


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient', 'disease_symptoms']

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['patient'].queryset = UserProfile.objects.filter(role=hms.models.patient)


class AvailabilityForm(forms.ModelForm):
    monday = 'Monday'
    tuesday = 'Tuesday'
    wednesday = 'Wednesday'
    thursday = 'Thursday'
    friday = 'Friday'
    saturday = 'Saturday'
    sunday = 'Sunday'

    DAY_CHOICES = [
        (monday, monday),
        (tuesday, tuesday),
        (wednesday, wednesday),
        (thursday, thursday),
        (friday, friday),
        (saturday, saturday),
        (sunday, sunday)
    ]

    days = forms.ChoiceField(choices=DAY_CHOICES)

    class Meta:
        model = DoctorsAvailibility
        fields = ['days', 'starting_time', 'ending_time', 'active']

        widgets = {
            "starting_time": forms.TextInput(
                attrs={"data_icon": "fa fa-calender", "required": "required", "type": "time"}),
            "ending_time": forms.TextInput(
                attrs={"data_icon": "fa fa-calender", "required": "required", "type": "time"}),
            "active": CheckboxInput()

        }

    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        self.fields['active'].label = "Active:"

    def save(self, commit=True):
        instance = super(AvailabilityForm, self).save(commit=False)
        days = self.cleaned_data.get('days')
        setattr(instance, f"{days}_start_time", self.cleaned_data.get('starting_time'))
        setattr(instance, f"{days}_end_time", self.cleaned_data.get('ending_time'))
        setattr(instance, f"{days}_active", self.cleaned_data.get('active'))
        print(instance)
        if commit:
            instance.save()
        return instance


class AdminAvailabilityForm(forms.ModelForm):
    monday = 'Monday'
    tuesday = 'Tuesday'
    wednesday = 'Wednesday'
    thursday = 'Thursday'
    friday = 'Friday'
    saturday = 'Saturday'
    sunday = 'Sunday'

    DAY_CHOICES = [
        (monday, monday),
        (tuesday, tuesday),
        (wednesday, wednesday),
        (thursday, thursday),
        (friday, friday),
        (saturday, saturday),
        (sunday, sunday)
    ]

    days = forms.ChoiceField(choices=DAY_CHOICES)

    class Meta:
        model = DoctorsAvailibility
        fields = ['doctor', 'days', 'starting_time', 'ending_time', 'active']

        widgets = {
            "starting_time": forms.TextInput(
                attrs={"data_icon": "fa fa-calender", "required": "required", "type": "time"}),
            "ending_time": forms.TextInput(
                attrs={"data_icon": "fa fa-calender", "required": "required", "type": "time"}),
            # "active": CheckboxInput()
            'active': forms.CheckboxInput(
                attrs={
                    'class': 'my-checkbox-class',
                    'id': 'my-checkbox-id',
                    'checked': True  # Set an initial value for the checkbox
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AdminAvailabilityForm, self).__init__(*args, **kwargs)
        self.fields['active'].label = "Active:"


class SlotsForm(forms.ModelForm):
    month = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'month'}))

    class Meta:
        model = Slots
        fields = ['doctor', 'month']

        # widgets = {
        #     "month": forms.DateTimeInput(
        #         attrs={'format': '%Y-%m', 'type': 'month'}
        #     )
        # }


class EditSlotForm(forms.ModelForm):
    class Meta:
        model = Slots
        fields = ['doctor', 'slot_date', 'slot_start_time', 'slot_end_time', 'is_available']
        widgets = {
            'slot_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'slot_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'slot_end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), widget=forms.Select(attrs={'id': 'doctor'}))
    slots = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'id': 'slots'}))

    class Meta:
        model = Appointment
        fields = ['doctor', 'slots', 'patient']

    def __init__(self, *args, **kwargs):
        appointment = kwargs.get('instance', None)
        if appointment:
            doctor_queryset = Doctor.objects.filter(id=appointment.slots.doctor.id)
        else:
            doctor_queryset = Doctor.objects.all()

        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = doctor_queryset
        self.fields['slots'].choices = []

        if 'doctor' in self.data:
            try:
                doctor_id = int(self.data.get('doctor'))
                slots = Slots.objects.filter(doctor_id=doctor_id, is_available=True)
                choices = [(slot.id,
                            slot.slot_start_time.strftime('%H:%M %p') + ' - ' + slot.slot_end_time.strftime('%H:%M %p'))
                           for slot in slots]
                self.fields['slots'].choices = choices
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['slots'].choices = [(self.instance.slots.id, str(self.instance.slots))]

    def clean(self):
        cleaned_data = super().clean()
        slots = cleaned_data.get('slots')
        if slots:
            cleaned_data['slots'] = Slots.objects.get(id=slots)
        return cleaned_data


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['doctor', 'patient', 'diagnosis', 'treatment', 'note']
