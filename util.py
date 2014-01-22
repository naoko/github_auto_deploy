import os


def read_key_file(path_to_pub_key_file):
    """
    return pub file string
    """
    key_file = os.path.expanduser(path_to_pub_key_file)
    if not key_file.endswith('pub'):
        raise RuntimeWarning('Trying to push non-public part of key pair')
    with open(key_file) as f:
        return f.read()