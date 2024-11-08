import socket
import os
import sys

def save_file(file_name, response):
    with open(file_name, 'wb') as file:
        file.write(response)


def split_command(command):
    parts = command.strip().split()

    operation = parts[0]
    file_path = parts[1]

    return operation, file_path


def create_http_post_request(filepath):
    request = (f"POST {filepath} HTTP/1.1\r\n\r\n")
    return request


def create_http_get_request(filepath):
    request = f"GET {filepath} HTTP/1.1\r\n"
    return request


def main(input_file, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        with open(input_file, "r") as file:
            for line in file:
                operation, file_path = split_command(line)

                if operation == "client_get":
                    request = create_http_get_request(file_path)
                elif operation == "client_post":
                    request = create_http_post_request(file_path)
        
                client_socket.send(request.encode()[:1048576])

                response = client_socket.recv(1048576)

                if operation == "client_get":
                    # print("Response from Get request: ", response.decode())
                    file_name = os.path.basename(file_path)
                    print(response)
                    save_file(file_name, response)

                elif operation == "client_post":
                    # print("Response from post request:", response.decode())
                    pass

if __name__ == "__main__":
    server_ip = sys.argv[1]
    port_number = int(sys.argv[2])

    input_file = "commands.txt"
    main(input_file, server_ip, port_number)
