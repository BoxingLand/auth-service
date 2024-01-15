from password_strength import PasswordPolicy


async def password_validation(
        password: str
) -> bool or list:
    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=1,  # need min. 1 uppercase letters
        # need min. 1 non-letter characters (digits, specials, anything)
        nonletters=1,
    )
    return policy.test(password=password)
#     if len(policy.test(password)):
#         return True
#     return False


if __name__ ==  '__main__':
    print(password_validation('Ttdf'))
