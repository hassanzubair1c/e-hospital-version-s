import calendar

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm, UserLoginForm, UserEditForm, DoctorForm, PatientForm, AvailabilityForm, \
    AdminAvailabilityForm, SlotsForm, EditSlotForm
from django.contrib.auth.models import User
from . import models as hospital_models, tables as hospital_tables
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from . import utils as hms_utils
from datetime import timedelta, datetime, time
from django.http import HttpResponse
from django import forms


# Create your views here.


def admin_dashboard(request):
    context = {
        'li_class': 'dashboard'
    }
    return render(request, 'dashboard/main.html', context)


def patient_register(request):
    if request.method == "POST":
        registered_from = request.GET.get('reg', 0)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cnic = request.POST.get('cnic')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
            user.set_password(password)
            user.save()
            user_profile = hospital_models.UserProfile.objects.create(cnic=cnic, user=user,
                                                                      role=hospital_models.patient)
            hospital_models.Patient.objects.create(patient=user_profile)
            if registered_from == 'admin':
                if user is not None and user_profile.role == hospital_models.patient:
                    auth_login(request, user)
                    return redirect('patient-data')
            else:
                return redirect('patient-login')
        else:
            messages.error("Your Passwords are not matching.")

    form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'PatientRegister.html', context)


def patient_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        user1 = User.objects.get(email=email)
        role = user1.userprofile.role
        if user is not None and role == hospital_models.patient:
            auth_login(request, user)
            return redirect('patient-disease')
        else:
            messages.error(request, "Email or password is not correct")
    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'patientlogin.html', context)


def doctor_register(request):
    if request.method == "POST":
        registered_from = request.GET.get('reg', 0)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cnic = request.POST.get('cnic')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
            user.set_password(password)
            user.save()
            user_profile = hospital_models.UserProfile.objects.create(cnic=cnic, user=user, role=hospital_models.doctor)
            hospital_models.Doctor.objects.create(doctor=user_profile)
            if registered_from == 'admin':
                if user is not None and user_profile.role == hospital_models.doctor:
                    auth_login(request, user)
                    return redirect('doctor-data')
            else:
                return redirect('doctor-login')
        else:
            messages.error("Your Passwords are not matching.")

    form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'doctorRegister.html', context)


def doctor_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        user1 = User.objects.get(email=email)
        role = user1.userprofile.role
        if user is not None and role == hospital_models.doctor:
            auth_login(request, user)
            return redirect('doctors_speciality')
        else:
            messages.error(request, "Email or password is not correct")
    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'doctorlogin.html', context)


def admin_register(request):
    if request.method == "POST":
        registered_from = request.GET.get('reg', 0)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cnic = request.POST.get('cnic')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
            user.set_password(password)
            user.save()
            user_profile = hospital_models.UserProfile.objects.create(cnic=cnic, user=user, role=hospital_models.admin)
            if registered_from == 'admin':
                if user is not None and user_profile.role == hospital_models.admin:
                    auth_login(request, user)
                    return redirect('admin-data')
            else:
                return redirect('admin-login')
        else:
            messages.error("Your passwords are not matching.")

    form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'admin_register.html', context)


@csrf_exempt
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        user1 = User.objects.get(email=email)
        role = user1.userprofile.role
        if user is not None and role == hospital_models.admin:
            auth_login(request, user)
            return redirect('admin-dashboard')
        else:
            messages.error(request, "Email or password is not correct")
    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'admin_login.html', context)


def admin_data(request):
    data = hospital_models.UserProfile.objects.filter(role=hospital_models.admin)
    datatable = hospital_tables.AdminTable(data)
    context = {
        'li_class': 'admin',
        'title': 'Admin Table',
        'table': datatable,
        'links': [
            {
                'title': 'Add Admin',
                'href': reverse('admin-register')
            }
        ]
    }
    return render(request, 'dashboard/dashboard_tables.html', context)


def edit_admin(request, pk):
    object = hospital_models.User.objects.get(id=pk)
    if request.method == "POST":
        usereditform = UserEditForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cnic = request.POST.get('cnic')
        object.first_name = first_name
        object.last_name = last_name
        object.email = email
        object.save()

        object = hospital_models.UserProfile.objects.filter(user=object).last()

        object.cnic = cnic
        object.save()

        return redirect('admin-data')

    form = UserEditForm(
        initial={'first_name': object.first_name, 'last_name': object.last_name, 'email': object.email,
                 'cnic': object.userprofile.cnic})
    context = {
        'form': form
    }
    return render(request, 'admin_edit_form.html', context)


def delete_admin(request, pk):
    object = hospital_models.User.objects.filter(id=pk)
    object.delete()
    return redirect('admin-data')


def patient_data(request):
    data = hospital_models.UserProfile.objects.filter(role=hospital_models.patient)
    datatable = hospital_tables.PatientTable(data)
    context = {
        'li_class': 'patient',
        'title': 'Patient Table',
        'table': datatable,
        'links': [
            {
                'title': 'Add Patient',
                'href': reverse('patient-register')
            }
        ]
    }
    return render(request, 'dashboard/dashboard_tables.html', context)


def edit_patient(request, pk):
    object = hospital_models.User.objects.get(id=pk)
    if request.method == "POST":
        usereditform = UserEditForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cnic = request.POST.get('cnic')
        object.first_name = first_name
        object.last_name = last_name
        object.email = email
        object.save()

        object = hospital_models.UserProfile.objects.filter(user=object).last()

        object.cnic = cnic
        object.save()

        return redirect('patient-data')

    form = UserEditForm(
        initial={'first_name': object.first_name, 'last_name': object.last_name, 'email': object.email,
                 'cnic': object.userprofile.cnic})
    context = {
        'form': form
    }
    return render(request, 'patient_edit_form.html', context)


def delete_patient(request, pk):
    object = hospital_models.User.objects.filter(id=pk)
    object.delete()
    return redirect('patient-data')


def doctor_data(request):
    data = hospital_models.UserProfile.objects.filter(role=hospital_models.doctor)
    datatable = hospital_tables.DoctorTable(data)
    context = {
        'li_class': 'doctor',
        'title': 'Doctor Table',
        'table': datatable,
        'links': [
            {
                'title': 'Add Doctor',
                'href': reverse('doctor-register')
            }
        ]
    }
    return render(request, 'dashboard/dashboard_tables.html', context)


def edit_doctor(request, pk):
    object = hospital_models.User.objects.get(id=pk)
    if request.method == "POST":
        usereditform = UserEditForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cnic = request.POST.get('cnic')
        object.first_name = first_name
        object.last_name = last_name
        object.email = email
        object.save()

        object = hospital_models.UserProfile.objects.filter(user=object).last()

        object.cnic = cnic
        object.save()

        return redirect('doctor-data')

    form = UserEditForm(
        initial={'first_name': object.first_name, 'last_name': object.last_name, 'email': object.email,
                 'cnic': object.userprofile.cnic})
    context = {
        'form': form
    }
    return render(request, 'doctor_edit_form.html', context)


def delete_doctor(request, pk):
    object = hospital_models.User.objects.get(id=pk)
    object.delete()
    return redirect('doctor-data')


@login_required(login_url='doctor-login')
@user_passes_test(hms_utils.is_doctor)
def doctor_speciality(request):
    userprofile = request.user.userprofile
    if userprofile.role == hospital_models.doctor:
        print(userprofile.role)
        if request.method == "POST":
            doctorform = DoctorForm(request.POST)
            if doctorform.is_valid():
                doctorform.save()
                return redirect("availibility")

    form = DoctorForm()
    context = {
        'form': form
    }
    return render(request, 'doctor_speciality.html', context)


@login_required(login_url='patient-login')
def patient_disease(request):
    userprofile = request.user.userprofile
    if userprofile.role == hospital_models.patient:
        if request.method == "POST":
            patientform = PatientForm(request.POST)
            if patientform.is_valid():
                patientform.save()

    form = PatientForm()
    context = {
        'form': form
    }
    return render(request, 'patient_disease.html', context)


@login_required(login_url='doctor-login')
def avalibility(request):
    doctor = request.user.userprofile.doctor_profile.all().first()
    if request.method == "POST":
        availibilityform = AvailabilityForm(request.POST)
        if availibilityform.is_valid():
            # Retrieve doctor's existing availability for the selected day
            selected_day = availibilityform.cleaned_data['days']
            existing_availability = hospital_models.DoctorsAvailibility.objects.filter(doctor=doctor,
                                                                                       days=selected_day).first()

            # Check for conflicts with existing availability
            if existing_availability:
                start_time = availibilityform.cleaned_data['starting_time']
                end_time = availibilityform.cleaned_data['ending_time']

                if start_time >= existing_availability.starting_time and start_time < existing_availability.ending_time:
                    raise forms.ValidationError("This availability conflicts with an existing availability.")

                if end_time > existing_availability.starting_time and end_time <= existing_availability.ending_time:
                    raise forms.ValidationError('This availability conflicts with an existing availability.')

            # Save the new availability
            availibility = availibilityform.save(commit=False)
            availibility.doctor = doctor
            availibility.save()
    form = AvailabilityForm()
    context = {
        'form': form
    }
    return render(request, 'availibilityform.html', context)


def admin_side_avalibility(request):
    try:
        doctor = request.user.userprofile.doctor_profile.all().first()
    except ObjectDoesNotExist:
        return HttpResponse("User does not have a profile")

    if request.method == "POST":
        adminavailibilityform = AdminAvailabilityForm(request.POST)
        if adminavailibilityform.is_valid():
            new_availability = adminavailibilityform.save(commit=False)
            new_availability.doctor = doctor
            start_time = new_availability.starting_time
            end_time = new_availability.ending_time
            existing_availability_slots = hospital_models.DoctorsAvailibility.objects.filter(doctor=doctor, days=new_availability.days)

            for existing_availability in existing_availability_slots:
                if start_time >= existing_availability.starting_time and start_time < existing_availability.ending_time:
                    raise forms.ValidationError('This availability conflicts with an existing availability.')

                if end_time > existing_availability.starting_time and end_time <= existing_availability.ending_time:
                    raise forms.ValidationError('This availability conflicts with an existing availability.')

            new_availability.save()
            return redirect('availability-data')
    else:
        form = AdminAvailabilityForm()
        context = {
            'form': form
        }
        return render(request, 'admin_availability.html', context)


def doctor_availability_data(request):
    data = hospital_models.DoctorsAvailibility.objects.all()
    datatable = hospital_tables.AvailibilityTable(data)
    context = {
        'li_class': 'doctor',
        'title': 'Doctor Availability',
        'table': datatable,
        'links': [
            {
                'title': 'Add Doctor Availability',
                'href': reverse('admin-availibility')
            }
        ]
    }
    return render(request, 'dashboard/dashboard_tables.html', context)


def edit_availability(request, pk):
    object = hospital_models.DoctorsAvailibility.objects.get(id=pk)
    if request.method == "POST":
        availibilityform = AvailabilityForm(request.POST, instance=object)
        if availibilityform.is_valid():
            availibilityform.save()
            return redirect("availability-data")
    form = AvailabilityForm(instance=object)
    context = {
        'form': form
    }
    return render(request, 'availibilityform.html', context)


def delete_availibility(request, pk):
    object = hospital_models.DoctorsAvailibility.objects.get(id=pk)
    object.delete()
    return redirect('availability-data')


# def booked_appointment(request):
#     current_month = datetime.datetime.now().month
#     appointment = hospital_models.Appointment.objects.filter(starting_time__month=current_month)
#     data_table = hospital_tables.AppointmentTable(appointment)
#     context = {
#         'table': data_table
#     }
#     return render(request, 'booked_appointment.html', context)

def doctor_slots(request):
    try:
        if request.method == 'POST':
            form = SlotsForm(request.POST)
            year_month = request.POST.get('month')  # Here we are getting year and month from doctor
            doctor_id = request.POST.get('doctor')  # Here we are getting who is doctor
            doctor = hospital_models.Doctor.objects.get(
                id=doctor_id)  # In this ORM we are getting id of doctor from Doctor model
            available_days = doctor.doctorsavailibility_set.all()  # Here we are backtracking and getting doctor availability all data by going from doctor foreign key which is present in doctor availability form
            month = int(year_month.split('-')[1])  # Here we are splitting month from year_month we are getting
            available_slots = hospital_models.Slots.objects.filter(doctor=doctor,
                                                                   slot_date__month=month)  # In this ORM we are filtering all the slots which are available od doctor with there months
            # In this if statement we are saying that check if the length of available slots is zero which means that if there are no slots of that month then run all the code in that if statement otherwise don't create if there are slots with that month os that doctor
            if len(available_slots) == 0:
                for days in available_days:  # Here we are taking every object of doctor availability
                    day_name = days.days  # Here we are getting days from doctor availability model
                    starting_time = days.starting_time  # Here we are getting starting time from doctor availability model
                    ending_time = days.ending_time  # Here we are getting ending time from doctor availability model
                    day_number = list(calendar.day_name).index(
                        day_name)  # Here we are getting day number from calender library for example if we have monday it will give us 0 index numb for it and if sunday then 6
                    date = year_month  # Here we are getting year_month in a variable name date so we can split it
                    year = int(date.split('-')[
                                   0])  # In this year variable we are splitting year from the year month we are getting from user
                    month = int(date.split('-')[
                                    1])  # In this year variable we are splitting year from the year month we are getting from user
                    month_matrix = calendar.monthcalendar(year,
                                                          month)  # In this month matrix variable we will check the dates of the day we are getting from doctor availability in year and month which user gave us
                    dates = []  # In this empty list we will append all the dates we are getting of that particular day in that particular year and month
                    for week in month_matrix:
                        if week[int(day_number)] >= 1:
                            dates.append(week[int(day_number)])

                    list_dates = []  # In this empty list we will append the list of dates we are getting in dates list with there months and years
                    for date in dates:
                        list_dates.append(f'{year}-{month}-{date}')

                    for date in list_dates:  # In this loop we will pick all the dates in list_date one by one
                        start_datetime = datetime.strptime(f'{date} {starting_time}',
                                                           '%Y-%m-%d %H:%M:%S')  # Here we will change the date and start time from string to datetime
                        end_datetime = datetime.strptime(f'{date} {ending_time}',
                                                         '%Y-%m-%d %H:%M:%S')  # Here we will change the date and end time from string to datetime
                        slot_datetime = start_datetime
                        while slot_datetime < end_datetime:  # Now we will use while loop that this loop should run untill start time is equal to end time
                            slot_end_datetime = slot_datetime + timedelta(
                                minutes=15)  # Here by using timedelta function of datetime we are telling to make 15 min slots
                            slot_start_time = slot_datetime.strftime(
                                '%H:%M:%S')  # Here we are changing the datetime again into string
                            slot_end_time = slot_end_datetime.strftime(
                                '%H:%M:%S')  # Here we are changing the datetime again into string
                            slot_date = slot_datetime.strftime(
                                '%Y-%m-%d')  # Here we are changing the datetime again into string

                            new_slot = hospital_models.Slots.objects.create(doctor=doctor, slot_date=slot_date,
                                                                            slot_start_time=slot_start_time,
                                                                            slot_end_time=slot_end_time)  # Here by using create ORM we are creating the slots and saving it in database
                            slot_datetime = slot_end_datetime
                return HttpResponse("Success")
            else:
                return HttpResponse("Slots already available for this month")
        else:
            form = SlotsForm()
            context = {
                'form': form
            }
            return render(request, 'slotform.html', context)
    except Exception as e:
        print(e)
        return HttpResponse("Error")


def slot_data(request):
    data = hospital_models.Slots.objects.all()
    datatable = hospital_tables.SlotTable(data)
    context = {
        'li_class': 'doctor',
        'title': 'Slots Table',
        'table': datatable,
        'links': [
            {
                'title': 'Add Single Slot',
                'href': reverse('add-slot')
            }
        ]
    }
    return render(request, 'dashboard/dashboard_tables.html', context)


def edit_slot(request, pk):
    object = hospital_models.Slots.objects.get(id=pk)
    if request.method == "POST":
        editslotform = EditSlotForm(request.POST, instance=object)
        if editslotform.is_valid():
            # Get the start and end time of the edited slot
            slot_start_time = editslotform.cleaned_data.get('slot_start_time')
            slot_end_time = editslotform.cleaned_data.get('slot_end_time')

            # Calculate the duration between the start and end time
            duration = (datetime.combine(datetime.min, slot_end_time) - datetime.combine(datetime.min, slot_start_time)).total_seconds() / 60

            # Check if the duration is not equal to 15 minutes
            if duration != 15:
                raise ValidationError("Slot duration must be exactly 15 minutes.")

            # Save the edited slot if it is valid
            editslotform.save()
            return redirect("slot-data")
    form = EditSlotForm(instance=object)
    context = {
        'form': form
    }
    return render(request, 'slotform.html', context)


def delete_slot(request, pk):
    object = hospital_models.Slots.objects.get(id=pk)
    object.delete()
    return redirect('slot-data')


def add_single_slot(request):
    if request.method == "POST":
        single_slot_form = EditSlotForm(request.POST or None)
        doctor_id = request.POST.get('doctor')
        doctor = hospital_models.Doctor.objects.get(id=doctor_id)
        slot_date = request.POST.get('slot_date')
        slot_start_time_str = request.POST.get('slot_start_time')
        slot_end_time_str = request.POST.get('slot_end_time')
        is_available_str = request.POST.get('is_available')
        is_available = True if is_available_str == 'true' else False

        if single_slot_form.is_valid():
            # Convert slot start and end times to datetime.time objects
            slot_start_time = datetime.strptime(slot_start_time_str, '%H:%M:%S').time()
            slot_end_time = datetime.strptime(slot_end_time_str, '%H:%M:%S').time()

            # Calculate the duration between the start and end time
            duration = (datetime.combine(datetime.min, slot_end_time) - datetime.combine(datetime.min, slot_start_time)).total_seconds() / 60

            # Check if the duration is not equal to 15 minutes
            if duration != 15:
                raise ValidationError("Slot duration must be exactly 15 minutes.")

            # Create the new slot object
            new_slot = hospital_models.Slots.objects.create(doctor=doctor, slot_date=slot_date,
                                                            slot_start_time=slot_start_time,
                                                            slot_end_time=slot_end_time, is_available=is_available)
            return redirect("slot-data")

    form = EditSlotForm()
    context = {
        'form': form
    }
    return render(request, 'slotform.html', context)

