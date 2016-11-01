__author__ = 'ajay'

from django.core.validators import RegexValidator

CITIES = (
    (None, '---Select Your Current City---'),
    ('Narela', 'Narela'),
    ('Gurgaon', 'Gurgaon'),
    ('Delhi', 'Delhi'),
    ('Noida', 'Noida'),
    ('Faridabad', 'Faridabad'),
)

PHONE_REG = RegexValidator(regex=r'^[789]\d{9}$', message="Enter a valid 10 digit phone number.")

USER_TYPE = [
    ('Listener', 'Listener'),
    ('Musician', 'Musician')
]

GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female')
]
REFRESH_TIME_IN_MINUTES = 30

# TODO: should be moved to settings file
ACCESS_FROM_REFRESH_URL = 'http://localhost:8000/auth/token'