from rest_framework.validators import ValidationError


def validate_me_username(value):
    if value.lower() == "me":
        raise ValidationError("Invalid username: 'me' is not allowed.")
    return value
