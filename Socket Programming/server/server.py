import socket
import threading
import os
import sys
import mimetypes

# Function to handle client POST request
def handle_POST(path: str, data: str):
    # get file name
    file_name = os.path.basename(path)
    print(file_name)
    with open(file_name, "wb") as f:
        # Write data into the file
        f.write(data)
    # Send 200 OK response
    response = "HTTP/1.1 200 OK\r\n\r\n"
    return response.encode()

# Function to handle client GET request
def handle_GET(path: str):
    file_path = path.lstrip("/")  # Remove leading "/"
    
    # Check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Detect the MIME type and set the content type
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"
        
        # Read the file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Create the HTTP response with Content-Length and Content-Type headers
        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: {mime_type}\r\n"
            f"Content-Length: {len(file_content)}\r\n"
            f"Connection: close\r\n\r\n"
        )
        
        # Send the headers followed by the content
        return response.encode() + file_content
    else:
        # Send 404 Not Found response
        response = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
        return response.encode()


def handle_client(client_socket: socket.socket, addr:tuple):
    try:

        while True:
            # Receive client messages
            request = client_socket.recv(1048576)

            # Indicate close listen socket
            if not request:
                break

            # Split the request into headers and body
            headers, body = request.split(b"\r\n\r\n", 1)
            headers = headers.decode('utf-8')
            
            # Now `body` contains the content after the blank line
            print("Headers:\n", headers)
            print("Body:\n", body)
            
            # Get request command
            lines = headers.splitlines()
            request_line = lines[0]
            method, path, _ = request_line.split()

            # Handle GET and POST requests
            if method == "GET":
                response = handle_GET(path=path)
            elif method == "POST":
                response = handle_POST(path=path, data=body)
            
            # Send response to client
            client_socket.send(response)
    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server(port =8000):  # default server port
    server_ip = "127.0.0.1"  # default server's IP address
    # create a socket object
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connection
        server.listen()
        print(f"Listing on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            client_socket.settimeout(10)

            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            # handle client function with client socket and client address
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    # get port number from arguments input
    port = int(sys.argv[1]) # server port number

    # run server
    run_server(port=port)