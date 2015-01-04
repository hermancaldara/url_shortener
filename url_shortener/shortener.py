import hashlib


def string_shortener(str, quantity_chars=7):
    return hashlib.sha1(str).hexdigest()[:quantity_chars]
