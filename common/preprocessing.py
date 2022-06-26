import string


def process(string: str):
    string = string.lower()
    clean_string = [s for s in string if s.isalnum() or s.isspace()]
    return ''.join(clean_string)
