import re
def is_valid_password(password):
    # At least 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    # Must contain uppercase, lowercase, digit, special char
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    if re.search(r"\s", password):
        return False, "Password must not contain spaces."

    return True, ""

