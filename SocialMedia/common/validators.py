from django.core.exceptions import ValidationError
from django.utils import timezone


def mobile_validator(mobile):
    if mobile[0:2] != '09':
        raise ValidationError('Please follow the mentioned format')


def mobile_length_validator(mobile):
    if len(mobile) != 11:
        raise ValidationError('Please follow the mentioned format:invalid length')


def national_code_length_validator(national_code):
    if len(national_code) != 10:
        raise ValidationError('%(national_code)s has invalid length', params={'national_code': national_code})


def validate_not_empty(value):
    if value == '':
        raise ValidationError('{} is empty!'.format(value))
