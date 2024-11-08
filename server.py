import socket
import threading
import os

# Function to handle client POST request
def handle_POST(path: str, data: str):
    file_path = path.lstrip("/")  # Remove leading "/"
    os.makedirs(file_path, exist_ok=True)  # Ensure directory exists
    with open(file_path + "/file.txt", "w") as f:
        # Write data into the file
        f.write(data)
    # Send 200 OK response
    response = "HTTP/1.1 200 OK\r\n"
    return response.encode()

# Function to handle client GET request
def handle_GET(path: str):
    file_path = path.lstrip("/")  # Remove leading "/"
    # Check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Read the file content
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Send 200 OK response with file content
        response = "HTTP/1.1 200 OK\r\n"
        return response.encode() + file_content
    else:
        # Send 404 Not Found response
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        return response.encode()

def handle_client(client_socket: socket.socket, addr:tuple):
    try:
        # Receive client messages
        request = client_socket.recv(1024).decode("utf-8")
        
        print(f"Received: {request}")
        
        # Get request command
        lines = request.splitlines()
        request_line = lines[0]
        method, path, _ = request_line.split()
        
        # Get data if the method is POST
        data = lines[-1]
        
        # Handle GET and POST requests
        if method == "GET":
            response = handle_GET(path=path)
        elif method == "POST":
            response = handle_POST(path=path, data=data)
        
        # Send response to client
        client_socket.send(response)
    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def run_server(port = 8000):
    server_ip = "127.0.0.1" # default server's IP address
    # creat a socket object
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incomming connection
        server.listen()
        print(f"Listing on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            # handle client function with client socket and client address
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()