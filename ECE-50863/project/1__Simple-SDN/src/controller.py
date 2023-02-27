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

class Network:
    """
    Class
    ----------
    Network clas
        - Store the network topology
        - Routes by widest path (max bottleneck capacity)
    """

    def __init__(self, file_name):
        """
        Function
        ----------
        Initialization function to parse network topology
        

        Parameters
        ----------
        file_name : str
            Config file name
        """

        # File Handling
        try: CFG = open(file_name, 'r')
        except: SYS.exit('\n    [ Error ] File does not exist / Wrong file name.\n')
        self.CFG = CFG.read().split('\n')
        
        for i in range(len(self.CFG)):
            line = self.CFG[i]

            if len(line) <= 0: continue

            # Topology Initialization
            if i == 0: 
                self.nodes = int(line)

                self.node = {i: True for i in range(self.nodes)}
                self.topology = {i: {} for i in range(self.nodes)}

            # Attach Bandwidth to Each Link
            else:
                split_result = list(map(int, line.split()))
                src, dest, bw = split_result[0], split_result[1], split_result[2]

                self.topology[src][dest] = bw
                self.topology[dest][src] = bw

        CFG.close()

        self.ori_topology = dict(self.topology)

    def _retrieve_path(self, parent, node, target, path):
        """
        Function
        ----------
        Retrieve routing path after computing the routing path
        

        Parameters
        ----------
        parent : list
            Parent node for each child nodes
        node: int
            Source node ID
        target: int
            Destination node ID
        path: list
            Routing path record
        """

        # No result for offline node
        if node == -1: return 

        self._retrieve_path(parent, parent[node], target, path)
        path.append(node)

    def widest_path_routing(self, src, dest):
        """
        Function
        ----------
        Algorightm of Widest Path Routing
        

        Parameters
        ----------
        src : int
            Source node ID
        dest: int
            Destination node ID
        """
        
        max_bandwidth = [float('-inf')] * self.nodes
        max_bandwidth[src] = float('inf')
        parent = [-1] * self.nodes
        
        queue = [(0, src)]

        while queue:
            tmp = queue.pop()
            current_node = tmp[1]

            if current_node not in self.topology: continue

            for neighbor in self.topology[current_node]:
                bw = self.topology[current_node][neighbor]
                cost = max(max_bandwidth[neighbor], min(max_bandwidth[current_node], bw))

                if cost > max_bandwidth[neighbor]:
                    max_bandwidth[neighbor] = cost
                    parent[neighbor] = current_node

                    queue.append((cost, neighbor))
                    queue = sorted(queue)

        path = []
        self._retrieve_path(parent, dest, dest, path)

        return path, max_bandwidth[dest]
    
    def compute_path(self):
        """
        Function
        ----------
        Compute each path by Widest Path Routing
        """

        self.route_path = {}

        output = '{0}\nRouting Update'.format(get_timestamp())
        print(output)
        log(LOG_FILE, output)
        for src in range(self.nodes):
            # Offline Source Node
            if not self.node[src]: continue

            self.route_path[src] = {}

            for dest in range(self.nodes):
                if src == dest:
                    self.route_path[src][dest] = (dest, 9999)

                # Offline Destination Node
                elif not self.node[dest]: 
                    self.route_path[src][dest] = (-1, 0)

                else:
                    path, cost = self.widest_path_routing(src, dest)
                    
                    if cost != float('-inf'): self.route_path[src][dest] = (path[1], cost) 

                    # No Path to Reach Destination
                    else: self.route_path[src][dest] = (-1, 0) 

                output = '{0},{1}:{2},{3}'.format(src, dest, 
                                                  self.route_path[src][dest][0], 
                                                  self.route_path[src][dest][1]
                                                 )
                print(output)
                log(LOG_FILE, output)
        
        output = 'Routing Complete'
        print(output)
        log(LOG_FILE, output)

    def connect_node(self, id):
        """
        Function
        ----------
        Add node and links to the topology when node is alive again
        

        Parameters
        ----------
        id : int
            Alive node ID
        """
        
        self.node[id] = True

        self.topology[id] = {}

        for line in self.CFG[1:]:
            split_result = list(map(int, line.split()))
            src, dest, bw = split_result[0], split_result[1], split_result[2]

            if src == id: 
                self.topology[id][dest] = bw
                # if self.node[dest]: self.topology[dest][id] = bw
            
            if dest == id: 
                self.topology[id][src] = bw
                # if self.node[src]: self.topology[src][id] = bw

    def connect_link(self, node1, node2):
        """
        Function
        ----------
        Add links to the topology when link is alive again
        

        Parameters
        ----------
        node1 : int
            One of node in the link
        node2 : int
            One of node in the link
        """

        for line in self.CFG[1:]:
            split_result = list(map(int, line.split()))
            src, dest, bw = split_result[0], split_result[1], split_result[2]

            if (src == node1 and dest == node2) or (src == node2 and dest == node1):
                if self.node[node1] and self.node[node2]: self.topology[node1][node2] = bw

    def remove_node(self, id):
        """
        Function
        ----------
        Remove node and links from the topology when node is offline
        

        Parameters
        ----------
        id : int
            Alive node ID
        """

        self.node[id] = False

        del self.topology[id]

        for node in self.topology:
            if id in self.topology[node]: del self.topology[node][id]

    def remove_link(self, src, dest):
        """
        Function
        ----------
        Remove links from the topology when link is offline
        

        Parameters
        ----------
        node1 : int
            One of node in the link
        node2 : int
            One of node in the link
        """

        if self.node[src] and self.node[dest]: del self.topology[src][dest]

    def get_node_status(self, id):
        """
        Function
        ----------
        Get node's status (alive or offline) for TIMEOUT check
        

        Parameters
        ----------
        id : int
            Node ID
        """

        return self.node[id]

    def get_route_path(self):
        """
        Function
        ----------
        Return routing path for 'Route Update' message
        """

        return self.route_path

    def get_topology(self):
        """
        Function
        ----------
        Return topology for neighbor nodes information in 'Register Response' message
        """

        return self.topology

    def get_nodes_number(self) -> int:
        return self.nodes

class System:
    """
    Class
    ----------
    System clas
        - Record network topology from system level
    """

    def __init__(self):
        self.status = False

        self.switch_info = {}
        self.switch_msg  = {}

        self.node_alive = []
        self.link_alive = []
        self.link_dead  = []

    def bootstrap(self, num_nodes, timestamp):
        """
        Function
        ----------
        (1) Mark bootstrap when len(switch_info) == Network.get_nodes_number()
        (2) Give each switch a initial timestamp for TIMEOUT checking

        Parameters
        ----------
        num_nodes : int
            Total Number of Switches
        timestamp : obj
            datetime object
        """

        self.status = True
        
        for i in range(num_nodes):
            self.switch_msg[i] = {}
            self.switch_msg[i]['timestamp'] = timestamp

    def add_switch_info(self, id, node_info):
        """
        Function
        ----------
        Add switch's (host / post) information from 'Register Request' message

        Parameters
        ----------
        id : int
            Switch ID
        node_info : tuple
            (Switch Host, Switch Port)
        """

        self.switch_info[id] = node_info

    def update_switch_msg(self, id, timestamp, neighbor):
        """
        Function
        ----------
        Update switch's timestamp and neighbor information from 'Toplogy Update' message

        Parameters
        ----------
        id : int
            Switch ID
        timestamp : obj
            datetime object
        neighbor : dict
            Switch's Neighbor Information (Alive or not)
        """

        self.switch_msg[id] = {'timestamp': timestamp, 'neighbor': neighbor}

    def remove_switch(self, id):
        """
        Function
        ----------
        Mark switch is offline when switch is offline (timestamp delta > 6 seconds)

        Parameters
        ----------
        id : int
            Switch ID
        """

        del self.switch_info[id]
        del self.switch_msg[id]

    def get_status(self):
        """
        Function
        ----------
        (1) Check whether system is in bootstrap status
        (2) For switch alive condition, status is True but still receive 'Register Request' message
        """

        return self.status

    def get_node_alive(self):
        return self.node_alive

    def get_link_alive(self):
        return self.link_alive

    def get_link_dead(self):
        return self.link_dead

    def get_num_switch(self):
        """
        Function
        ----------
        For Bootstrap Process (Check whether all switches are registered)
        """

        return len(self.switch_info)

    def get_switch_info(self):
        """
        Function
        ----------
        For sending 'Register Response' & 'Route Update' message
        """

        return self.switch_info

    def get_switch_msg(self):
        """
        Function
        ----------
        (1) For 'Topology Update' to check link alive of link offline
        (2) Check for TIMEOUT
        """

        return self.switch_msg

class Recv(THREAD.Thread):
    """
    Class
    ----------
    Recv class (child class of Thread)
        - Receive messages from switches
        - Update network topology according to the received messages
    """

    def __init__(self, socket, network, system):
        THREAD.Thread.__init__(self)
       
        self.socket = socket
        
        self.network = network
        self.system = system

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
            sender_id = int(msg_data['id'])
            node_info = data[1]
            
            # =======================================================
            #  'Register Request' Message (from Switches)           =
            # =======================================================
            if msg_data['type'] == 0:
                self.system.add_switch_info(sender_id, node_info)
                
                output = '{0}\nRegister Request {1}'.format(get_timestamp(), msg_data['id'])
                print(output)
                log(LOG_FILE, output)

                # Switch Alive Condition
                if not self.network.get_node_status(sender_id):
                    self.system.switch_msg[sender_id] = {}
                    self.system.switch_msg[sender_id]['timestamp'] = DATETIME.datetime.now()

                    self.system.get_node_alive().append(sender_id)

            # =======================================================
            #  'Topology Update' Message (from Switches)            = TODO
            # =======================================================
            if msg_data['type'] == 1:
                # Retrieve old record to check Link Alive or Offline
                msg_record = dict(self.system.get_switch_msg())

                # Update Switch Message Record
                self.system.update_switch_msg(sender_id, DATETIME.datetime.now(), msg_data['neighbor'])

                # Check for New Topology Update Information
                if 'neighbor' in msg_record[sender_id]:
                    neighbors = sorted(msg_data['neighbor'].keys())

                    # =======================================================
                    #  Link is Offline / Alive (Notified by Switches)       =
                    # =======================================================
                    for neighbor in neighbors:
                        if (msg_data['neighbor'][neighbor] == True)  and (msg_record[sender_id]['neighbor'][neighbor] == False):
                            self.system.get_link_alive().append((sender_id, int(neighbor)))

                        if (msg_data['neighbor'][neighbor] == False) and (msg_record[sender_id]['neighbor'][neighbor] == True):
                            self.system.get_link_dead().append((sender_id, int(neighbor)))

class Send(THREAD.Thread):
    """
    Class
    ----------
    Send class (child class of Thread)
        - Send messages to switches
    """

    def __init__(self, socket, network, system):
        THREAD.Thread.__init__(self)

        self.socket = socket

        self.network = network
        self.system = system

    def run(self):
        # =======================================================
        #  'Bootstrap' Process                                  =
        # =======================================================
        while not self.system.get_status():
            if self.system.get_num_switch() == self.network.get_nodes_number():
                self.system.bootstrap(self.network.get_nodes_number(), DATETIME.datetime.now())

                # 'Register Response' Message (to All Switches)
                output = get_timestamp()
                print(output)
                log(LOG_FILE, output)
                for id in range(self.network.nodes):
                    self.reg_response(id)

                self.network.compute_path()
                route_path = self.network.get_route_path()

                # 'Route Update' Message (to All Switches)
                self.route_update(route_path)

        while True:
            # =======================================================
            #  Check for Alive Node                                 =
            # =======================================================
            if self.system.get_node_alive():
                node = self.system.get_node_alive().pop()
                self.network.connect_node(node)

                output = '{0}\nSwitch Alive {1}'.format(get_timestamp(), node)
                print(output)
                log(LOG_FILE, output)

                # Update Routing Path
                self.network.compute_path()
                route_path = self.network.get_route_path()

                # 'Register Response' Message (to Alive Switch and its neighbors)
                for switch in range(self.network.nodes):
                    if switch == node or (switch in route_path and node in route_path[switch]): 
                        output = get_timestamp()
                        print(output)
                        log(LOG_FILE, output)
                        self.reg_response(switch)

                # 'Route Update' Message (to All Switches)
                self.route_update(route_path)

            # =======================================================
            #  Check for Offline Link                               =
            # =======================================================
            if self.system.get_link_dead():
                src, dest = self.system.get_link_dead().pop()
                self.network.remove_link(src, dest)

                output = '{0}\nLink Dead {1},{2}'.format(get_timestamp(), src, dest)
                print(output)
                log(LOG_FILE, output)

                # Update Routing Path
                self.network.compute_path()
                route_path = self.network.get_route_path()

                # 'Route Update' Message (to Switches)
                self.route_update(route_path)

            # =======================================================
            #  Check for Alive Link                                 =
            # =======================================================
            if self.system.get_link_alive():
                src, dest = self.system.get_link_alive().pop()
                self.network.connect_link(src, dest)

                print('{0}\nLink Alive {1},{2}'.format(get_timestamp(), src, dest))

                # Update Routing Path
                self.network.compute_path()
                route_path = self.network.get_route_path()

                # 'Route Update' Message (to Switches)
                self.route_update(route_path)

            # =======================================================
            #  Check TIMEOUT for Each Switch                        =
            # =======================================================
            for id in range(self.network.nodes):
                if not self.network.get_node_status(id): continue

                # Switch is Offline
                if DATETIME.datetime.now() - self.system.get_switch_msg()[id]['timestamp'] >= DATETIME.timedelta(seconds=6):
                    # Remove Switch Info (Host / Port) & Msg (TimeStamp / Neighbor) from System
                    self.system.remove_switch(id)

                    # Remove Node from Network Topology
                    self.network.remove_node(id)

                    output = '{0}\nSwitch Dead {1}'.format(get_timestamp(), id)
                    print(output)
                    log(LOG_FILE, output)

                    # Update Routing Path
                    self.network.compute_path()
                    route_path = self.network.get_route_path()

                    # 'Route Update' Message (to Switches)
                    self.route_update(route_path)

    def reg_response(self, id):
        """
        Function
        ----------
        Send 'Register Response' message
        """

        switch_system_info = self.system.get_switch_info()
        
        neighbor = {}
        for element in self.network.ori_topology[id]: 
            if element in switch_system_info:
                neighbor[element] = (True, switch_system_info[element])
            else:
                neighbor[element] = (False, ('', ''))

        self.socket.sendto(JSON.dumps({'type': 0, 'neighbor': neighbor}).encode('utf-8'), 
                           switch_system_info[id])

        output = 'Register Response {0}'.format(id)
        print(output)
        log(LOG_FILE, output)

    def route_update(self, route_path):
        """
        Function
        ----------
        Send 'Route Update' message
        """

        switch_system_info = self.system.get_switch_info()

        # Send Routing Information to Each Switch
        for id in switch_system_info:
            self.socket.sendto(JSON.dumps({'type': 1, 'route_path': route_path}).encode('utf-8'), 
                               switch_system_info[id])

def main():
    # Argument Check
    if len(SYS.argv) != 3: SYS.exit('\n    [ Error ] Incorrect input.\n')

    port = int(SYS.argv[1])
    host = ""

    # Read Config to Build Network Topology
    network = Network(SYS.argv[2])
    system = System()

    # Log Purpose
    global LOG_FILE
    LOG_FILE = open('Controller.log', 'w', buffering=1)
    for i in range(network.get_nodes_number()):
        FILE = open('switch{0}.log'.format(i), 'w')
        FILE.close()
    
    # Socket Initialization
    sockfd = SOCKET.socket(SOCKET.AF_INET, SOCKET.SOCK_DGRAM, SOCKET.IPPROTO_UDP)
    sockfd.setsockopt(SOCKET.SOL_SOCKET, SOCKET.SO_REUSEADDR, 1)
    sockfd.bind((host, port))

    send_thread = Send(sockfd, network, system)
    recv_thread = Recv(sockfd, network, system)

    send_thread.start()
    recv_thread.start()

if __name__ == '__main__':
    main()