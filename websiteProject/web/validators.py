import re

from django.core.exceptions import ValidationError


class TextAndNumsOnlyValidator:

    def __init__(self, text):
        self.text = text

    def validate(self):
        special_symbols = re.compile(r'[^\w_]+')
        if special_symbols.search(self.text):
            raise ValidationError("Only letters, numbers and underscores are allowed in the username")

    def __eq__(self, other):
        return True