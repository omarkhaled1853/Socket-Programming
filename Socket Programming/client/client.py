import socket
import os
import sys
import mimetypes


def save_file(file_path, content):
    filename = os.path.basename(file_path)
    with open(filename, 'wb') as file:
        file.write(content)


def split_command(command):
    parts = command.strip().split()

    operation = parts[0]
    file_path = parts[1]
    host = parts[2]
    port = 80

    if len(parts) == 4:
        port = int(parts[3])

    return operation, file_path, host, port


def get_content_type_from_path(file_path):
    mime_type, encoding = mimetypes.guess_type(file_path)

    if mime_type:
        return mime_type
    else:
        return "unknown/unknown"


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Read the entire file content as a string
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()  # Read the entire file content as bytes
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def create_http_get_request(filepath, host):
    request = f"GET {filepath} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    return request.encode()


def create_http_post_request(file_path, host):
    content_type = get_content_type_from_path(file_path)
    if content_type == "unknown/unknown":
        raise ValueError("Invalid content type.")

    if content_type[: 5] == "image":
        body = read_binary_file(file_path)
    elif content_type[: 4] == "text":
        body = read_file(file_path).encode()
    else:
        raise ValueError("Invalid content type.")

    headers = (f"POST {file_path} HTTP/1.1\r\n"
               f"Host: {host}\r\n"
               f"Content-Length: {len(body)}\r\n"
               f"Content-Type: {content_type}\r\n\r\n")

    return headers.encode() + body


def client_logic(client_socket, input_file, host):
    with open(input_file, "r") as file:
        for line in file:
            operation, file_path, _, _ = split_command(line)

            if operation == "client_get":
                request = create_http_get_request(file_path, host)
            elif operation == "client_post":
                request = create_http_post_request(file_path, host)

            client_socket.sendall(request)

            response = client_socket.recv(1048576)

            headers, body = response.split(b"\r\n\r\n", 1)
            headers = headers.decode('utf-8')

            if operation == "client_get":
                print("Headers:\n", headers)
                print("Body:\n", body)
                save_file(file_path, body)

            elif operation == "client_post":
                print("Headers:\n", headers)


def main(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        while True:
            input_file = input("Please enter command file or exit to close connection: ")

            if input_file == "exit":
                break

            client_logic(client_socket, input_file, host)


if __name__ == "__main__":
    server_ip = sys.argv[1]
    port_number = int(sys.argv[2])

    # input_file = "commands.txt"
    main(server_ip, port_number)
