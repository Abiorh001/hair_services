from django.utils.crypto import get_random_string


def generate_random_string(length=100):
    """
    Generate a random string of length characters.
    """
    return get_random_string(length)
