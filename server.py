import socket


def run_server():
    # create soket object)
    # AF_INET (IPv4), AF_INEFT6 (IPv6)
    # SOCK_STREAM (TCP)
    # SOCK_DGRAM (UDP)
    # RAW_SOCKET (own transportation layer protocol)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # binding server socket to IP address and port number
    # localhost 127.0.0.1
    # port variable 8000 or any value above 1023
    server_ip = "127.0.0.1"
    port = 8000

    # prepare the socket to recieve connections
    # bind the socket to a specific address and port
    server.bind((server_ip, port))

    # listening for incoming connections
    # backlog argument -> specifies the maximum number of queued unaccepted connections
    # 0 means single client can interact with server
    # once accept is called a client is removed from queue
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    # accepting incoming connections
    # returns (conn, address)
    # address is tuple of ip address and port number (client)
    # conn is a new socket object (client)
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # creating communication loop
    # infinit loop
    # data recieved from client in binary form
    # decode binary form -> string form
    # break loop when close message is sent from client
    # recive data from the client
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # convert to string

        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8")) # convert to binary
            break
        
        print(f"Received: {request}")

        # sending response back to client
        response = "accepted".encode("utf-8") # convert to binary
        client_socket.send(response)
    
    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()

run_server()

