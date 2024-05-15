import socket
from utils import *
from ntru import NTRUKey, generate_key
import pickle

N = 5
p = 3
q = 2051


class server:

    def __init__(self, km):
        self.registered_clients = {}
        self.km = km
        self.n = 0
        self.deln = 100

    def add_client(self, id, K, n):
        self.registered_clients[id] = [K, n]


def main():

    HN = server(567890)

    #  add random clients

    HN.add_client(234562345, 3452345, 1005)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print("Server listening on {}:{}".format(host, port))

    client_socket, addr = server_socket.accept()
    print("Connection from {}".format(addr))

    # send_list(client_socket, [N,p,q,[2,3]])
    keys = generate_key()
    server_h = keys._h

    client_socket.sendall(pickle.dumps(server_h))
    client_pk = pickle.loads(client_socket.recv(8192))
    # client_pk = receive_list(client_socket)
    # print("Client Public Key", client_pk)
    # print(keys.get_h)

    # print(client_pk)
    # print(type(client_pk))


    # response = receive_list(client_socket)
    response = pickle.loads(client_socket.recv(5120000))
    response = keys.decrypt(response)
    response = deserialize(response)
    # print(type(response),"hii")
    # print(response)

    kn = response[1] ^ response[2] ^ HN.km
    id = response[1] ^ hash_function([HN.km, kn])
    c = hash_function([HN.km, id])

    if id not in HN.registered_clients.keys():
        abort()
    # print(id, HN.km, kn,"\n\n\n")
    K = HN.registered_clients[id][0]
    n_ = HN.registered_clients[id][1]

    if response[0] == 1:

        rn = response[3] ^ response[1] ^ id
        n = response[4] ^ hash_function([K, rn, response[3]])
        flag = False

        while n:
            if (
                hash_function([K, id, c, response[1], response[2], n, response[4]])
                == response[5]
            ):
                n_ = n
                flag = True
                break
            n -= 1
        if not flag:
            abort()
    elif response[0] == 0:
        flag = False
        n = n_
        while n >= n_:
            if hash_function([K, id, c, response[1], response[2]]) == response[3]:
                n_ = N
                flag = True
                break
            n -= 1
        if not flag:
            abort()
    else:
        abort()

    n_ = n_ + 1
    kn_ = get_random()
    fn_ = get_random()
    an_ = id ^ hash_function([HN.km, kn_])
    bn_ = an_ ^ HN.km ^ kn_
    eeta = hash_function([fn_, c]) ^ an_
    muu = hash_function([c, fn_]) ^ bn_
    alpha = c ^ fn_
    seskey = hash_function([K, fn_, eeta, muu, n_ + 1])
    beta = hash_function([seskey, an_, bn_, id, c])

    # send_list(client_socket, [alpha, beta, eeta, muu])
    # print(alpha, beta ,eeta ,muu)
    reply = serialize([alpha, beta, eeta, muu])
    # print(reply)
    # print(type(reply ))
    reply = keys.encrypt(reply, client_pk)
    client_socket.sendall(pickle.dumps(reply))

    print("Authentication Succesful")

    while True:

        data = client_socket.recv(1024).decode("utf-8")
        print("Received from client:", data)

        if data.lower() == "exit":
            break

        response = input("Enter message to send to client: ")
        client_socket.send(response.encode("utf-8"))

    client_socket.close()


if __name__ == "__main__":
    main()
