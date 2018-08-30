import random
from uuid import uuid4
from string import ascii_letters


def random_string(size=10, domain=ascii_letters):
    """
    Generates a random string of specific size using symbols from domain.
    """
    return ''.join([random.choice(domain) for _ in range(size)])


def random_uid():
    return str(uuid4())


def random_level():
    return random.randint(1, 100)
