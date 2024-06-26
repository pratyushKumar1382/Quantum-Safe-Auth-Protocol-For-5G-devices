import socket
from utils_server import *
import pickle


class server:

    def __init__(self, km):
        self.registered_clients = {}
        self.km = km
        self.n = 0
        self.deln = 100

    def add_client(self, id, K, n):
        self.registered_clients[id] = [K, n]


def main():

    # HN = server(567890)

    #  add random clients

    # HN.add_client(234562345, 3452345, 1005)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print("Server listening on {}:{}".format(host, port))

    client_socket, addr = server_socket.accept()
    print("Connection from {}".format(addr))

    # send_list(client_socket, [N,p,q,[2,3]])
    # keys = generate_key()
    # server_h = keys._h

    # client_socket.sendall(pickle.dumps(server_h))
    # client_pk = pickle.loads(client_socket.recv(8192))
    # client_pk = receive_list(client_socket)
    # print("Client Public Key", client_pk)
    # print(keys.get_h)


# **************** Registration Phase ****************
    print("Registration Phase\n")
    km = get_random()
    HN = server(km)
    # print(client_pk)
    # print(type(client_pk))
    K = get_random()
    kn = get_random()
    U_id = 234562345
    an = U_id ^ hash_function([km, kn])
    bn = an ^ km ^ kn
    c = hash_function([km, U_id])
    HN.add_client(U_id, K, 0)
    client_socket.sendall(pickle.dumps([K, U_id, an, bn, c]))
    print("Message sent from HN to UE [K, U_id, an, bn, cn]: ", [K, U_id, an, bn, c])



# **************** Phase 2 ****************
    print("\nAuthentication Phase\n")

    # response = receive_list(client_socket)
    response = pickle.loads(client_socket.recv(5120000))
    # response = keys.decrypt(response)
    # response = deserialize(response)
    # print(type(response),"hii")
    # print(response)

    kn = response[1] ^ response[2] ^ HN.km
    id = response[1] ^ hash_function([HN.km, kn])
    c = hash_function([HN.km, id])

    if id not in HN.registered_clients.keys():
        print("1")
        abort()
    # print(id, HN.km, kn,"\n\n\n")
    K = HN.registered_clients[id][0]
    n_ = HN.registered_clients[id][1]

    if response[0] == 1:    # desync mode

        # response[1] -> an
        # response[2] -> bn
        # response[3] -> yn
        # response[4] -> zn
        # response[5] -> hn
        print("Message recieved from UE [an, bn, yn, zn, hn] :", response)

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
        
    elif response[0] == 0:   # sync mode

        # response[1] -> an
        # response[2] -> bn
        # response[3] -> hn

        print("Message recieved from UE [an, bn, hn] :", response[1:])

        flag = False
        for itr in range(HN.deln):
            # print("hash ",[K, id, c, response[1], response[2], n])
            if hash_function([K, id, c, response[1], response[2], HN.registered_clients[id][1] + itr]) == response[3]:
                HN.registered_clients[id][1] = HN.registered_clients[id][1] + itr
                flag = True
                break
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
    print("\nSession Key :", seskey, "\n")
    beta = hash_function([seskey, an_, bn_, id, c])
    # print("hash",[seskey, an_, bn_, id, c])
    # print("hash", hash_function([seskey, an_, bn_, id, c]))


    # send_list(client_socket, [alpha, beta, eeta, muu])
    # print(alpha, beta ,eeta ,muu)
    # reply = serialize([alpha, beta, eeta, muu])
    reply = [alpha, beta, eeta, muu]
    # print(reply)
    # print(type(reply ))
    # reply = keys.encrypt(reply, client_pk)
    client_socket.sendall(pickle.dumps(reply))
    print("Message sent from HN to UE [alpha, beta, eeta, muu]: ", reply)

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
