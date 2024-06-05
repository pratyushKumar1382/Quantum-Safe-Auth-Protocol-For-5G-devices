import json
import hashlib
import random

host = "0.0.0.0"
port = 8004


def hash_function(lst):
    # Convert the list to a string representation
    list_str = ''.join(str(elem) for elem in lst)
    # Hash the string using SHA-512
    hash_object = hashlib.sha256(list_str.encode())
    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()
    # Convert the hexadecimal hash to an integer
    hash_int = int(hex_dig, 16)
    return hash_int


def abort():
    print("abborted")


def get_random():
    return random.randrange(1000000, 99999999, 1)





if __name__ == "__main__":
    print("utils")
