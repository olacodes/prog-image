import random
import string
import uuid


def generate_id():
    random_letter = random.choice(string.ascii_letters)
    uuid_hex = str(uuid.uuid4().hex)
    return f'{random_letter}{uuid_hex}'.lower()
