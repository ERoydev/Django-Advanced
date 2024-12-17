from django.core.exceptions import ValidationError
import re

def validate_username(value):
    # Regular expression for letters, numbers, and underscores
    if not re.match(r'^\w+$', value):
        raise ValidationError(
            "Ensure this value contains only letters, numbers, and underscore.",
            params={'value': value},
        )