from django.urls import path
from . import views as hospital_views

urlpatterns = [
    path('patient_register/', hospital_views.patient_register, name="patient-register"),
    path('patient_login/', hospital_views.patient_login, name="patient-login"),
    path('doctor_register/', hospital_views.doctor_register, name="doctor-register"),
    path('doctor_login/', hospital_views.doctor_login, name="doctor-login"),
    path('admin_register/', hospital_views.admin_register, name="admin-register"),
    path('admin_login/', hospital_views.admin_login, name="admin-login"),
    path('admin_dashboard/', hospital_views.admin_dashboard, name="admin-dashboard"),
    path('admin_data/', hospital_views.admin_data, name="admin-data"),
    path('patient_data/', hospital_views.patient_data, name="patient-data"),
    path('doctor_data/', hospital_views.doctor_data, name="doctor-data"),
    path('delete_admin/<int:pk>/', hospital_views.delete_admin, name="delete-admin"),
    path('delete_patient/<int:pk>/', hospital_views.delete_patient, name="delete-patient"),
    path('delete_doctor/<int:pk>/', hospital_views.delete_doctor, name="delete-doctor"),
    path('edit_admin/<int:pk>/', hospital_views.edit_admin, name="edit-admin"),
    path('edit_patient/<int:pk>/', hospital_views.edit_patient, name="edit-patient"),
    path('edit_doctor/<int:pk>/', hospital_views.edit_doctor, name="edit-doctor"),
    path('doctors_speciality/', hospital_views.doctor_speciality, name="doctors_speciality"),
    path('patient_disease/', hospital_views.patient_disease, name="patient-disease"),
    path('availibility/', hospital_views.avalibility, name="availibility"),
    path('doctor_availability_data/', hospital_views.doctor_availability_data, name="availability-data"),
    path('edit_availability/<int:pk>/', hospital_views.edit_availability, name="edit-availibility"),
    path('delete_availibility/<int:pk>/', hospital_views.delete_availibility, name="delete-availibility"),
    path('admin_side_availability/', hospital_views.admin_side_avalibility, name="admin-availibility"),
    path('doctor_slot/', hospital_views.doctor_slots, name="doctor-slot"),
    path('slots_data/', hospital_views.slot_data, name="slot-data"),
    path('delete_slot/<int:pk>/', hospital_views.delete_slot, name="delete-slot"),
    path('edit_slot/<int:pk>/', hospital_views.edit_slot, name="edit-slot"),
    path('add_single_slot/', hospital_views.add_single_slot, name="add-slot"),

]
