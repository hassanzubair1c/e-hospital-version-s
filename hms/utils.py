from . import models as hms_models
import base64
from PIL import Image
from io import BytesIO


def is_doctor(user):
    try:
        user: hms_models.User
        if user.userprofile.role == hms_models.doctor:
            return True
        return False
    except:
        return False


def is_patient(user):
    try:
        user: hms_models.User
        if user.userprofile.role == hms_models.patient:
            return True
        return False
    except:
        return False


def save_signature_image(signature_data):
    # Remove the data type declaration from the Base64 string
    data = signature_data.split(',')[1]

    # Decode the Base64 data
    decoded_data = base64.b64decode(data)

    # Create a PIL Image object from the decoded data
    image = Image.open(BytesIO(decoded_data))

    # Save the image to a file
    image.save('signature.png', 'PNG')

    return image

# Example usage:
