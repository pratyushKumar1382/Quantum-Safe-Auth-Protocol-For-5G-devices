import json
import hashlib
from poly import Polynomial as poly
from ntru import NTRUKey, generate_key
import hashlib
host = "127.0.0.1"
port = 8067


def receive_list(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    received_list = json.loads(data)
    return received_list

def send_list(client_socket, data_list):
    message = json.dumps(data_list)
    client_socket.send(message.encode('utf-8'))

# def serialize(message):
#     response = "@"
#     for mes in message:
#         response += (str(mes)+"#")
#     response += "@"
#     return response

def hash_function(lst):
    ans = len(lst)
    itr = 0
    while itr < len(lst):
        ans = ans ^ lst[itr] | itr
        itr += 1
    return ans
    # # Convert the list to a string representation
    # list_str = ''.join(str(elem) for elem in lst)
    
    # # Hash the string using SHA-512
    # hash_object = hashlib.sha256(list_str.encode())
    
    # # Get the hexadecimal representation of the hash
    # hex_dig = hash_object.hexdigest()
    
    # # Convert the hexadecimal hash to an integer
    # hash_int = int(hex_dig, 16)
    
    # return hash_int
    
    
def abort():
    return 0

def get_random():
    return 3

def deserialize(msg, ele=0):
    print(msg,"hii")
    lst = []
    for ms in msg:
        lst.append(ms)
    # print(lst,type(lst))
    itr = 0
    if ele:
        while len(lst) != ele*20:
            lst.append(0)
        
    response = []
    # print(len(lst))
    while itr < len(lst):
        itr1 = 0
        val = 0
        mul = 1
        while itr1<20 and itr+itr1<len(lst):
            addr = lst[itr+itr1]
            if addr == -1:
                addr = 2
            val += addr*mul
            mul *= 3
            itr1 += 1
            # print(itr1,"itr1")
        response.append(val)
        itr += 20
        # print(val)
    # print("return")
    return response
    

def serialize(msg):
    lst = []
    for ms in msg:
        itr = 0
        while itr<20:
            val = ms%3
            if val == 2:
                val = -1
            lst.append(val)
            itr+=1
            ms = int(ms/3)
            # print(val,ms)
    print(lst)
    return poly(lst,len(lst))

# def send_message(msg, pk, keys):
#     msg = serialize(msg)
#     msg = keys.encrypt(msg,pk)
#     return msg

# def recieve_message(msg, keys):
    

if __name__ == "__main__":
    print("utils")
    print(serialize([25,30,81]))