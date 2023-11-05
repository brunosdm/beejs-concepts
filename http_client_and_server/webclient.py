import socket
import sys
from constants import *

HTTP_REQUEST = "GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}"

class Response:
    def __init__(self, response: str):
        self.response = response

    def response(self):
        return self.response

    def header(self):
        return self.response.split("\r\n\r\n")[0]

    def body(self):
        return self.response.split("\r\n\r\n")[1]

def send_request_and_get_response(address: tuple, http_request: bytes) -> Response:
    
    def get_response(s: socket) -> Response:
        response = ""

        while True:
            partial_response = s.recv(RECV_BUFFER_SIZE).decode(ENCODING)

            if partial_response == "":
                break

            response += partial_response

        return Response(response)

    s = socket.socket()

    s.connect(address)

    s.sendall(http_request)

    return get_response(s)

def main():
    host = sys.argv[1]
    port = sys.argv[2]
    payload = ""
    
    if len(sys.argv) == 4:
        payload = sys.argv[3]

    address = (host, int(port))

    encoded_http_request = HTTP_REQUEST.format(host, len(payload), payload).encode(ENCODING)

    response = send_request_and_get_response(address, encoded_http_request)

    print(response.header())

if __name__ == "__main__":
    main()