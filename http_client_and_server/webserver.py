import socket
import sys
from constants import *

HTTP_RESPONSE = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"

def get_header_and_body(s: socket) -> tuple:

    def get_remaining_body(s: socket, remaining_content_length: int) -> str:
        remaining_body = ""

        if remaining_content_length > RECV_BUFFER_SIZE:
            buffer_sized_chunks = remaining_content_length // RECV_BUFFER_SIZE
            remainder = remaining_content_length % RECV_BUFFER_SIZE

            for _ in range(buffer_sized_chunks):
                remaining_body += s.recv(RECV_BUFFER_SIZE).decode(ENCODING)

            remaining_body += s.recv(remainder).decode(ENCODING)
        else:
            remaining_body += s.recv(remaining_content_length).decode(ENCODING)

        return remaining_body
    
    def get_content_length(header: str) -> int:
        if CONTENT_LENGTH_HEADER not in header:
            return 0

        length_str = header.split(CONTENT_LENGTH_HEADER + ": ")[1].split(CARRIAGE_RETURN)[0]

        return int(length_str)

    header = ""
    body = ""
    partial_request = ""

    while True:
        partial_request += s.recv(RECV_BUFFER_SIZE).decode(ENCODING)

        if DOUBLE_CARRIAGE_RETURN in partial_request:
            header_body_split = partial_request.split(DOUBLE_CARRIAGE_RETURN)
            header = header_body_split[0]
            body = header_body_split[1]
            break

    content_length_header_value = get_content_length(header)

    remaining_content_length = content_length_header_value - len(body)

    if remaining_content_length > 0:
        body += get_remaining_body(s, remaining_content_length)

    return header, body

def get_request_method_from_header(header: str) -> str:
    return header.split(" ")[0]

def start_server(s: socket) -> None:
    while True:
        new_conn = s.accept()

        new_socket = new_conn[0]
        addr = new_conn[1]

        print("New connection by [{}:{}]".format(addr[0], addr[1]))

        try:
            header, body = get_header_and_body(new_socket)

            print("Request method: {}".format(get_request_method_from_header(header)))

            print("Payload: {}\n".format(body))

            new_socket.sendall(HTTP_RESPONSE.encode(ENCODING))

        except Exception as error:
            print("Error when processing request!")
            print("Caused by: {} - {}\n".format(type(error).__name__, error))

        finally:
            new_socket.close()

def main():
    port = sys.argv[1]

    s = socket.socket()

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(("", int(port)))

    s.listen()

    start_server(s)

if __name__ == "__main__":
    main()