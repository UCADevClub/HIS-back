import re
from django.core.exceptions import ValidationError


def phone_number_validator(phone_number: str):
    """
    checks string for KG phone number pattern,
    excepts for O!, Beeline and MegaCom
    """
    pattern = r"996(7[5-5]\d{2}|22[0-9]\d{2}|99[9]\d{2}|77([0-37-9]\d{2}|5(58|9[7-9]))|(5[0157]|70)\d{3}|54(3\d{2}|59[5-6])|56(550|6(9\d|47|69|8[7-9]))|20[0-35]\d{2})\d{4}"
    match = re.fullmatch(pattern=pattern, string=phone_number)
    if not bool(match):
        raise ValidationError(phone_number)


def inn_validator(inn_string: str):
    pass
