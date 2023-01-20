from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number.'),
            params={'value': value},
        )


def validate_code(num):
    num = str(num)
    if len(num) != 2:
        raise ValidationError(
            _('%(value)s is more than two character.'),
            params={'value': num},
        )
    if not num.startswith('1'):
        raise ValidationError(
            _('%(value)s is not starting with 1.'),
            params={'value': num},
        )
    return True
