import re


def is_phone_number_correct(
        phone_number: str
) -> bool:
    pattern = r"^(?:\+7|8)\d{10}$"
    return re.match(pattern, phone_number) is not None
