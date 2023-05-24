from django.contrib import admin
from . import models as hospital_model

# Register your models here.
admin.site.register(hospital_model.UserProfile)
admin.site.register(hospital_model.Doctor)
admin.site.register(hospital_model.Patient)
admin.site.register(hospital_model.Slots)
admin.site.register(hospital_model.Appointment)
admin.site.register(hospital_model.DoctorsAvailibility)
admin.site.register(hospital_model.Diagnosis)
admin.site.register(hospital_model.Email)
