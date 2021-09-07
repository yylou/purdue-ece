import sys
import socket
import threading
import time
from time import sleep
DATABASE_DELAY = 10

class service_client(threading.Thread):
    '''
    Thread responsible for servicing the client request.
        - Receive the client request
        - Parse and process the client request
        - Fetch the file (from the current directory)
        - Read and send the file

    Args:
    '''

    def __init__(self, socket):
       threading.Thread.__init__(self)
       self.socket = socket

    def run(self):
        while True:
            try:
                data = self.socket.recv(1024)
            except:
                print("Unable to receive data")
                break

            data = data.decode('ascii')
            
            data = open('testfile.txt', 'r').read()

            time.sleep(DATABASE_DELAY)
            
            self.socket.send(data.encode('ascii'))

def main():
    num_args = len(sys.argv)
    if num_args < 2:
        print ("Usage: python server.py <port>\n")
        exit()
    
    port = int(sys.argv[1])
    host = ""

    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.bind((host, port))
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    print ("Socket binded to port ", port)

    sockfd.listen(3)

    # ====================================================================== #

    while True:
        clientfd, addr = sockfd.accept()

        newthread = service_client(clientfd)
        newthread.start()

    sockfd.close()

if __name__ == "__main__":
    main()