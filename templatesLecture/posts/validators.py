from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

def bad_language_validator(value):
    if value in ['badword1', 'badword2']:
        raise ValidationError('The text contains bad language!')

@deconstructible
class BadLanguageValidator:

    def __init__(self, bad_words=None):
        if bad_words is None:
            self.bad_words = ["badword1", "badword2"]

        else:
            self.bad_words = bad_words

    def __call__(self, value):
        for bad_word in self.bad_words:
            if bad_word.lower() in value.lower():
                raise ValidationError("The text contains bad language!")