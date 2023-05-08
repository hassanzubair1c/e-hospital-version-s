from . import models as hms_models


def is_doctor(user):
    try:
        user:hms_models.User
        if user.userprofile.role == hms_models.doctor:
            return True
        return False
    except:
        return False

def is_patient(user):
    try:
        user:hms_models.User
        if user.userprofile.role == hms_models.patient:
            return True
        return False
    except:
        return False



