import sys
import socket
import time

def main():
    num_args = len(sys.argv)
    if num_args < 4:
        print ("Usage: python client.py <server hostname> <server port> <client port>\n")
        sys.exit(1)

    server_hostname = sys.argv[1]
    ip_addr         = socket.gethostbyname(server_hostname)
    server_port     = int(sys.argv[2])
    my_port         = int(sys.argv[3])

    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.bind(('127.0.0.1', my_port))
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if __debug__:
        print ("Socket bind to port ", str(my_port))

    server_address = (server_hostname, server_port)
    sockfd.connect(server_address)
    if __debug__:
        print ("Socket connected to server @ ", str(server_address))

    message = "GET testfile.txt"
    sockfd.send(message.encode('ascii'))
    print(str(time.time()) + ' Sent to the server :\n' + message)

    data = sockfd.recv(4096)

    print(str(time.time()) + ' Received from the server :\n' + str(data.decode('ascii')))

main()