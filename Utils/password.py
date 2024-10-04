import re

import bcrypt


def validate_password(password1):
    if len(password1) < 8:
        return 0
    return 1


def check_password(password1, password2):
    if password1 and password1 == password2:
        return True
    else:
        return False


def get_hashed_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_hashed_passsword(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def password_validate_regex(password):
    regex = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[#@$%^&+=]).{8,}$'
    if re.match(regex, password):
        return True
    return False
