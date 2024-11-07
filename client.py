import socket
import os
import sys


def receive_response(socket):
    response = b""

    while True:
        data = socket.recv(1024)
        if not data:
            break
        response += data

    return response


def save_file(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)


def split_command(command):
    parts = command.strip().split()

    if len(parts) < 3:
        raise ValueError("Invalid command format.")

    operation = parts[0]
    file_path = parts[1]
    host = parts[2]
    port = 80

    if len(parts) == 4:
        port = int(parts[3])

    body = ""
    if operation == "client_post":
        body = " ".join(parts[4:])

    return operation, file_path, host, port, body


def create_http_post_request(filepath, body, host):
    request = (f"POST {filepath} HTTP/1.1\r\n"
               f"Host: {host}\r\n"
               f"Content-Length: {len(body)}\r\n"
               f"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
               f"{body}")

    return request


def create_http_get_request(filepath, host):
    request = f"GET {filepath} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    return request


def main(input_file, host, port):
    # Use 'with' to automatically handle the socket closing
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        with open(input_file, "r") as file:
            for line in file:
                operation, file_path, _, _, body = split_command(line)

                if operation == "client_get":
                    request = create_http_get_request(file_path, host)
                elif operation == "client_post":
                    request = create_http_post_request(file_path, body, host)

                client_socket.sendall(request.encode())

                response = receive_response(client_socket)

                if operation == "client_get":
                    print("Response from Get request: ", response.decode())
                    filename = os.path.basename(file_path)
                    save_file(filename, response)

                elif operation == "client_post":
                    print("Response from post request:", response.decode())


if __name__ == "__main__":
    # print(sys.argv[0])
    server_ip = sys.argv[1]
    port_number = int(sys.argv[2])

    # print(server_ip)
    # print(port_number)
    input_file = "commands.txt"
    main(input_file, server_ip, port_number)
