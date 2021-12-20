#
#    Author : Yuan-Yao Lou (Mike) <yylou@purdue.edu>
#    Title  : Ph.D. student in ECE at Purdue University
#    Date   : 2021/09/23
#


import os as OS
import sys as SYS
import json as JSON
import socket as SOCKET
import threading as THREAD
import datetime as DATETIME


def get_timestamp():
    return '\n\n{0:%H:%M:%S.%f}'.format(DATETIME.datetime.now())

def log(FILE, content):
    """
    Function
    ----------
    
    

    Parameters
    ----------
    
    
    """

    FILE.write('{0}\n'.format(content))

class Switch():
    """
    Class
    ----------
    Switch class
        - Store and process switch's neighbor nodes information
    """

    def __init__(self, fail_id):
        self.ready = False

        self.neighbor_info   = {}
        self.neighbor_status = {}
        self.neighbor_msg    = {}
        self.neighbor_alive  = []

        self.fail_id = str(fail_id)

    def bootstrap(self):
        """
        Function
        ----------
        For bootstrap process, mark all neighbors as alive
        """

        self.ready = True

    def get_status(self, id):
        """
        Function
        ----------
        Get node's status (alive or offline) for:
        (1) Switch alive condition (previously offline but receive KEEP_ALIVE to alive)
        (2) TIMEOUT check
        

        Parameters
        ----------
        id : int
            Node ID
        """

        return self.neighbor_status[id]

    def update_neighbor(self, neighbor):
        """
        Function
        ----------
        Update neighbor information from 'Resgister Response' message
        (1) Update each neighbor's (host / port) information
        (2) Give each switch a initial timestamp for TIMEOUT checking


        Parameters
        ----------
        neighbor : dict
            {str(ID): (Switch Host, Switch Port)}
        """

        self.neighbor_info = neighbor
        
        for element in self.neighbor_info:
            if self.neighbor_info[element][0]:
                self.neighbor_info[element]   = tuple(self.neighbor_info[element][1])
                if element not in self.neighbor_status or self.neighbor_status[element] == True:
                    self.neighbor_status[element] = True
                self.neighbor_msg[element]    = DATETIME.datetime.now()
            else:
                self.neighbor_status[element] = False

    def update_neighbor_info(self, id, host, port):
        """
        Function
        ----------
        Update neighbor information from 'Keep Alive' message
        (1) Update each neighbor's (host / port) information by id


        Parameters
        ----------
        id : dict
            Sender Switch ID
        host : str
            Sender Switch Host Name
        port : str
            Sender Switch port number
        """

        self.neighbor_info[id] = (host, port)

    def update_neighbor_status(self, id, status):
        """
        Function
        ----------
        Update neighbor status from 'Keep Alive' message
        (1) Update each neighbor's status (True: Alive, False: Offline)


        Parameters
        ----------
        id : dict
            Sender Switch ID
        status : bool
            Sender Switch Status
        """

        self.neighbor_status[id] = status

    def update_neighbor_msg(self, id, timestamp):
        """
        Function
        ----------
        Update neighbor status from 'Keep Alive' message
        (1) Update each neighbor's timestamp for status check


        Parameters
        ----------
        id : dict
            Sender Switch ID
        timestamp : datetime object
            Sender Switch TimeStamp
        """

        self.neighbor_msg[id] = timestamp

    def add_neighbor_alive(self, id):
        return self.neighbor_alive.append(id)

    def get_neighbors(self):
        return sorted(self.neighbor_status.keys())

    def get_neighbor_info(self):
        return self.neighbor_info

    def get_neighbor_status(self):
        return self.neighbor_status

    def get_neighbor_msg(self):
        return self.neighbor_msg

    def get_neighbor_alive(self):
        return self.neighbor_alive.pop()

    def is_any_alive(self):
        return True if self.neighbor_alive else False

class Recv(THREAD.Thread):
    """
    Class
    ----------
    Recv class (child class of Thread)
        - Receive messages from controller and neighbors
    """

    def __init__(self, socket, id, host, port, switch):
        THREAD.Thread.__init__(self)

        self.socket = socket

        self.id = str(id)
        self.controller_host = host
        self.controller_port = port

        self.switch = switch

    def run(self):
        while True:
            try:
                data = self.socket.recvfrom(1024)
            except:
                break

            # =======================================================
            #  Message Extraction                                   =
            # =======================================================
            msg_data = JSON.loads(data[0].decode('utf-8'))
            node_info = data[1]

            # =======================================================
            #  'Register Response' Message (from Controller)        =
            # =======================================================
            if msg_data['type'] == 0 and node_info[1] == self.controller_port:
                self.switch.update_neighbor(msg_data['neighbor'])

                output = '{0}\nRegister Response Received'.format(get_timestamp())
                print(output)
                log(LOG_FILE, output)

                self.switch.bootstrap()

            # =======================================================
            #  'Topology Update' Message (from Controller)          =
            # =======================================================
            if msg_data['type'] == 1 and node_info[1] == self.controller_port:
                route_path = msg_data['route_path']

                output = '{0}\nRouting Update'.format(get_timestamp())
                print(output)
                log(LOG_FILE, output)
                for neighbor in route_path[self.id]:
                    output = '{0},{1}:{2}'.format(self.id, neighbor, 
                                                  route_path[self.id][neighbor][0])
                    print(output)
                    log(LOG_FILE, output)
                output = 'Routing Complete'
                print(output)
                log(LOG_FILE, output)

            # =======================================================
            #  'Keep Alive' Message (from Neighbors)                =
            # =======================================================
            if msg_data['type'] == 2:
                id = msg_data['id']
                host = node_info[0]
                port = node_info[1]

                if id != self.switch.fail_id:
                    # Switch Alive
                    if not self.switch.get_status(id): 
                        self.switch.add_neighbor_alive(id)

                    self.switch.update_neighbor_info(id, host, port)
                    self.switch.update_neighbor_status(id, True)
                    self.switch.update_neighbor_msg(id, DATETIME.datetime.now())

class Send(THREAD.Thread):
    """
    Class
    ----------
    Send class (child class of Thread)
        - Send messages to controller and neighbors
    """

    def __init__(self, socket, id, host, port, switch):
        THREAD.Thread.__init__(self)

        self.socket = socket

        self.id = str(id)
        self.controller_host = host
        self.controller_port = port

        self.switch = switch

    def run(self):
        # =======================================================
        #  'Register Request' Message (to Controller)           =
        # =======================================================
        self.socket.sendto(JSON.dumps({'type': 0, 'id': self.id}).encode('utf-8'), 
                           (self.controller_host, self.controller_port))
        output = '{0}\nRegister Request Sent'.format(get_timestamp())
        print(output)
        log(LOG_FILE, output)

        # Wait for Bootstrap
        while not self.switch.ready: pass

        start_timestamp = DATETIME.datetime.now()

        while True:
            # =======================================================
            #  Check for Alive Neighbor                             =
            # =======================================================
            if self.switch.is_any_alive():
                id = self.switch.get_neighbor_alive()

                output = '{0}\nNeighbor Alive {1}'.format(get_timestamp(), id)
                print(output)
                log(LOG_FILE, output)

                # 'Topology Update' Message (to Controller)
                self.socket.sendto(JSON.dumps({'type': 1, 'id': self.id, 'neighbor': self.switch.get_neighbor_status()}).encode('utf-8'),
                                   (self.controller_host, self.controller_port))

            # =======================================================
            #  Check TIMEOUT for Each Switch                        =
            # =======================================================
            for id in list(self.switch.get_neighbors()):
                if not self.switch.get_status(id): continue

                # Switch is Offline
                if DATETIME.datetime.now() - self.switch.get_neighbor_msg()[id] >= DATETIME.timedelta(seconds=6):
                    # Modify Switch Status
                    self.switch.update_neighbor_status(id, False)

                    output = '{0}\nNeighbor Dead {1}'.format(get_timestamp(), id)
                    print(output)
                    log(LOG_FILE, output)

                    # =======================================================
                    #  'Topology Update' Message (to Controller)            =
                    # =======================================================
                    self.socket.sendto(JSON.dumps({'type': 1, 'id': self.id, 'neighbor': self.switch.get_neighbor_status()}).encode('utf-8'),
                                       (self.controller_host, self.controller_port))

            # Count for Every 2 Seconds
            if DATETIME.datetime.now() - start_timestamp >= DATETIME.timedelta(seconds=2):
                neighbor_info   = self.switch.get_neighbor_info()
                neighbor_status = self.switch.get_neighbor_status()

                # (debug)
                # print('ID: {0}, Neighbor Info: {1}, Neighbot Msg: {2}'.format(self.id, self.switch.neighbor_info, self.switch.neighbor_msg))

                # =======================================================
                #  'Keep Alive' Message (to Neighbors)                  =
                # =======================================================
                for neighbor in neighbor_info:
                    if not self.switch.get_status(neighbor): continue

                    if neighbor != self.switch.fail_id:
                        self.socket.sendto(JSON.dumps({'type': 2, 'id': self.id}).encode('utf-8'),
                                           neighbor_info[neighbor])
                
                # =======================================================
                #  'Topology Update' Message (to Controller)            =
                # =======================================================
                self.socket.sendto(JSON.dumps({'type': 1, 'id': self.id, 'neighbor': neighbor_status}).encode('utf-8'),
                                   (self.controller_host, self.controller_port))

                # Renew Start Timestamp for Next Messages
                start_timestamp = DATETIME.datetime.now()

def main():
    # Argument Check
    if len(SYS.argv) != 6 and len(SYS.argv) != 4: SYS.exit('\n    [ Error ] Incorrect input.\n')
    if len(SYS.argv) == 6 and '-f' not in SYS.argv: SYS.exit('\n    [ Error ] Incorrect input.\n')

    id = int(SYS.argv[1])
    host = SYS.argv[2]
    port = int(SYS.argv[3])

    # Check for Offline Neighbor
    offline_neighbor = ''
    if len(SYS.argv) == 6: offline_neighbor = SYS.argv[SYS.argv.index('-f') + 1]

    # Log Purpose
    global LOG_FILE
    LOG_FILE = open('switch{0}.log'.format(id), 'a', buffering=1)

    switch = Switch(offline_neighbor)

    sockfd = SOCKET.socket(SOCKET.AF_INET, SOCKET.SOCK_DGRAM, SOCKET.IPPROTO_UDP)
    sockfd.setsockopt(SOCKET.SOL_SOCKET, SOCKET.SO_REUSEADDR, 1)

    send_thread = Send(sockfd, id, host, port, switch)
    recv_thread = Recv(sockfd, id, host, port, switch)

    send_thread.start()
    recv_thread.start()

if __name__ == '__main__':
    main()