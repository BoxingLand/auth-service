import re


async def password_validation(
        password: str
) -> list:
    details: list = []
    
    if len(password) < 8:
        details.append("Lenght(8)")
    if not re.search(r'[A-Z]', password):
        details.append("Uppercase(1)")
    if not re.search(r'[^a-zA-Z]', password):
        details.append("NonLetter(1)")

    return details
