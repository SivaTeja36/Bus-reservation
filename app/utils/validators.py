from app.utils.constants import (
    ATLEAST_ONE_DIGIT, 
    ATLEAST_ONE_LOWER_CASE, 
    ATLEAST_ONE_SPECIAL_CHARACTER, 
    ATLEAST_ONE_UPPER_CASE, 
    SHOULD_NOT_CONTAIN_SPACES
)

#┌────────────────────────────── FIELD VALIDATIONS ──────────────────────────────────────────┐

def validate_password(password: str) -> str:
    """
        Custom password validation to ensure it meets security standards.
    """
    field_name = "Password"

    if not any(char.isupper() for char in password):
        raise ValueError(f"{field_name} {ATLEAST_ONE_UPPER_CASE}")
    if not any(char.islower() for char in password):
        raise ValueError(f"{field_name} {ATLEAST_ONE_LOWER_CASE}")
    if not any(char.isdigit() for char in password):
        raise ValueError(f"{field_name} {ATLEAST_ONE_DIGIT}")
    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
        raise ValueError(f"{field_name} {ATLEAST_ONE_SPECIAL_CHARACTER}")
    if " " in password:
        raise ValueError(f"{field_name} {SHOULD_NOT_CONTAIN_SPACES}")
    
    return password