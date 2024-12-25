from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы один специальный символ: " + "!@#$%^&*().?:{}|<>"),
                code='password_no_special',
            )

    def get_help_text(self):
        return _("Ваш пароль должен содержать хотя бы один специальный символ: " + "!@#$%^&*().?:{}|<>")


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну заглавную букву."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Ваш пароль должен содержать хотя бы одну заглавную букву.")


class LowercaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну строчную букву."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _("Ваш пароль должен содержать хотя бы одну строчную букву.")
