import socket

def run_client():
    # instantiating socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connecting to server socket
    server_ip = "127.0.0.1"
    server_port = 8000

    # establish connection with server
    client.connect((server_ip, server_port))

    # creating communication loop
    while True:
        # input message and send it to the server
        msg = input("Enter message: " )
        client.send(msg.encode("utf-8")[:1024])

        # handling server response
        # receive message from the server
        response = client.recv(1024)
        response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "closed":
            break

        print(f"Recieved: {response}")
    
    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()