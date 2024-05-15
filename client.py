import socket
from utils import *
from ntru import NTRUKey, generate_key
from poly import Polynomial as poly
import pickle
import sys
import time


class client:

    def __init__(self, K_, id_, n_, kn_, km_):
        self.K = K_
        self.id = id_
        self.n = n_
        self.kn = kn_
        self.km = km_
        self.an = id_ ^ hash_function([km_, kn_])
        # print(self.an ^ hash_function([km_, kn_]),"\n\n\n", km_, kn_)
        self.bn = self.an ^ km_ ^ kn_
        self.c = hash_function([km_, id_])

    def sync_message(self, str):
        # print([0, self.an, self.bn, hash_function([self.K, self.id, self.c, self.an, self.bn, self.n])],"\n\n\n\n")
        return [
            0,
            self.an,
            self.bn,
            hash_function([self.K, self.id, self.c, self.an, self.bn, self.n]),
        ]

    def desync_message(self, str):
        rn = get_random()
        yn = self.an ^ self.id ^ rn
        zn = hash_function([self.K, rn, yn])
        return [
            1,
            self.an,
            self.bn,
            yn,
            zn,
            hash_function([self.K, self.id, self.c, self.an, self.bn, self.n, zn]),
        ]


def main():

    mobile = client(3452345, 234562345, 1010, 23456, 567890)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print("Connected to server on {}:{}".format(host, port))
    server_pk = pickle.loads(client_socket.recv(8192))
    # print(server_pk)
    # print(type(server_pk))

    # print("Server Public Key", server_pk)
    
    start_time = time.perf_counter()

    keys = generate_key()
    client_h = keys._h
    client_socket.sendall(pickle.dumps(client_h))
    # # print(keys.get_h)
    # send(client_socket, client_h.coefficients())


    mode = "Sync"

    reply = mode
    if 0:
        reply = mobile.desync_message(mode)
        # send_list(client_socket, mobile.desync_message(mode))
    elif 1:
        reply = mobile.sync_message(mode)
        # send_list(client_socket, mobile.sync_message(mode))
    else:
        abort()

    # reply = send_message(reply, server_pk, keys)
    reply = serialize(reply)
    reply = keys.encrypt(reply, server_pk)
    sys.getsizeof(pickle.dumps(reply))
    client_socket.sendall(pickle.dumps(reply))

    mobile.n += 1

    # tokens = receive_list(client_socket)

    tokens = pickle.loads(client_socket.recv(5120000))
    tokens = keys.decrypt(tokens)
    tokens = deserialize(tokens, 4)
    # print(tokens)

    fn_ = mobile.c ^ tokens[0]
    an_ = tokens[2] ^ hash_function([fn_, mobile.c])
    bn_ = tokens[3] ^ hash_function([mobile.c, fn_])
    seskey = hash_function([mobile.K, fn_, tokens[2], tokens[3], (mobile.n) + 1])
    beta_ = hash_function([seskey, an_, bn_, mobile.id, mobile.c])

    if beta_ == tokens[1]:
        abort()

    end_time = time.perf_counter()
    
    
    print("Authentication Successful")
    
    print("Time Taken in Auth: ", end_time - start_time, "s")

    while True:

        message = input("Enter message to send to server (type 'exit' to quit): ")
        client_socket.send(message.encode("utf-8"))

        if message.lower() == "exit":
            break

        response = client_socket.recv(1024).decode("utf-8")
        print("Received from server:", response)

    client_socket.close()


if __name__ == "__main__":
    main()
