import secrets
import string

def generate_activation_token(length=32):
    """Generate a random activation token."""
    characters = string.ascii_letters + string.digits
    activation_token = ''.join(secrets.choice(characters) for _ in range(length))
    return activation_token
