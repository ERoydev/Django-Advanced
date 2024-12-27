from unittest import TestCase

from django.core.exceptions import ValidationError

from posts.validators import BadLanguageValidator


class TestBadLanguageValidator(TestCase):
    def test__bad_words_included__raises_validationError(self):
        validator = BadLanguageValidator()

        with self.assertRaises(ValidationError) as ve:
            validator('badword1')

        self.assertEqual(
            "['The text contains bad language!']",
            str(ve.exception)
        )