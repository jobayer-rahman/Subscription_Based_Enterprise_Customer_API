from django.test import TestCase
from .utils import validate_code

from django.core.exceptions import ValidationError

class ValidateCodeTest(TestCase):
    # for utils.validate_code function
    def test_validate_code(self):
        # Test valid input
        self.assertTrue(validate_code(11))

        # Test input with length greater than 2
        with self.assertRaises(ValidationError) as cm:
            validate_code(123)
        self.assertEqual(cm.exception.messages.pop(), '123 is more than two character.')

        # Test input that does not start with 1
        with self.assertRaises(ValidationError) as cm:
            validate_code(21)
        self.assertEqual(cm.exception.messages.pop(), "21 is not starting with 1.")




