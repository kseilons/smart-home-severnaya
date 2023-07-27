import random
import string


def random_string(string_length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(string_length))
