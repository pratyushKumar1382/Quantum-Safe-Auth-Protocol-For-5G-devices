import socket
from utils_client import *
import pickle
import time


class client:

    def __init__(self, K_, id_, n_, an_, bn_, c_):
        self.K = K_
        self.id = id_
        self.n = n_
        self.an = an_
        # print(self.an ^ hash_function([km_, kn_]),"\n\n\n", km_, kn_)
        self.bn = bn_
        self.c = c_

    def sync_message(self, str):
        # print("hash: ", [self.K, self.id, self.c, self.an, self.bn, self.n])
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

    # mobile = client(3452345, 234562345, 1010, 23456, 567890)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print("Connected to server on {}:{}".format(host, port))
    # server_pk = pickle.loads(client_socket.recv(8192))
    # print(server_pk)
    # print(type(server_pk))

    # print("Server Public Key", server_pk)
    

# **************** Registration Phase ****************
    start_time = time.perf_counter()

    # response[0] -> K
    # response[1] -> id
    # response[2] -> an
    # response[3] -> bn
    # response[4] -> c


    response = pickle.loads(client_socket.recv(5120000))
    mobile = client(response[0], response[1], 0, response[2], response[3], response[4])




    # keys = generate_key()
    # client_h = keys._h
    # client_socket.sendall(pickle.dumps(client_h))
    # # print(keys.get_h)
    # send(client_socket, client_h.coefficients())

    end_time = time.perf_counter()

    print("Time taken in Registration Phase: ",end_time - start_time, " s")


# **************** Phase 1 ****************
    start_time = time.perf_counter()



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
    # reply = serialize(reply)
    # reply = keys.encrypt(reply, server_pk)
    # sys.getsizeof(pickle.dumps(reply))
    # print(reply)
    client_socket.sendall(pickle.dumps(reply))


# **************** Phase 3 ****************


    mobile.n += 1

    # tokens[0] -> alpha
    # tokens[1] -> beta
    # tokens[2] -> eeta
    # tokens[3] -> muu

    tokens = pickle.loads(client_socket.recv(5120000))
    # tokens = keys.decrypt(tokens)
    # tokens = deserialize(tokens, 4)
    # print(tokens)

    fn_ = mobile.c ^ tokens[0]
    an_ = tokens[2] ^ hash_function([fn_, mobile.c])
    bn_ = tokens[3] ^ hash_function([mobile.c, fn_])
    seskey = hash_function([mobile.K, fn_, tokens[2], tokens[3], (mobile.n) + 1])
    beta_ = hash_function([seskey, an_, bn_, mobile.id, mobile.c])
    # print(["hash", seskey, an_, bn_, mobile.id, mobile.c])
    # print("hash", hash_function([ seskey, an_, bn_, mobile.id, mobile.c]))


    if beta_ != tokens[1]:
        abort()

    end_time = time.perf_counter()

    print("Time taken in Auth Phase: ",end_time - start_time, " s")

    
    
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
