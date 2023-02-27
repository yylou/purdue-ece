#!/usr/bin/env python3
#
#    Author : Yuan-Yao Lou (Mike) <yylou@purdue.edu>
#    Title  : Ph.D. student in ECE at Purdue University
#    Date   : 2021/10/19
#


from monitor import Monitor

import sys as SYS
import configparser as CONFIGPARSER
import datetime as DATETIME
import time as TIME
import threading as THREAD
import socket as SOCKET


def log(msg):
    """
    System Log Information

    Parameters
    ----------
    msg : str
        message for logging purpose
    """
    
    print('{0:<30} |{1:<5}{2}'.format(str(DATETIME.datetime.now()), ' ', msg))


def split_content(FILE, MAX_size_packet, size_header):
    """
    Split file content into chunks for sending packets

    Parameters
    ----------
    FILE : obj
        file object

    MAX_size_packet : int
        MAX packet size

    size_header : int
        packet header size
    """

    content = FILE.read().encode('utf-8')
    index   = 0
    seq_num = 0
    packets = {}

    while True:
        encode_seq_num = str.encode(f'{seq_num}|', 'ascii')
        size_packet = MAX_size_packet - size_header - len(encode_seq_num)

        # EOF
        if index + size_packet > len(content):
            packets[seq_num] = encode_seq_num + content[index:]
            break

        packets[seq_num] = encode_seq_num + content[index:index+size_packet]

        index   += size_packet
        seq_num += 1

    FILE.close()

    return packets


class System():
    """
    Sender System Information: Connection Status, Packet Sequence Number, Packet Record, Timeout
    """

    def __init__(self, monitor, config, packets, send_id, recv_id, size_packet):
        self.monitor        = monitor
        self.send_id        = send_id
        self.recv_id        = recv_id
        self.packet_size    = size_packet

        self.active         = True          # System is active (connected w/ receiver)
        self.seq_num        = 0             # Packet sequence number
        self.packets        = packets       # Packets ready to be sent
        
        # Calculate and set timeout value to Minitor
        timeout             = 1.65 * (int(config.get("network", "MAX_PACKET_SIZE")) / int(config.get("network", "LINK_BANDWIDTH")) + 2 * float(config.get("network", "PROP_DELAY")))
        self.timeout        = max(0.38, min(0.65, timeout))
        self.monitor.socketfd.settimeout(self.timeout)

    def send(self, debug=False):
        """
        Send packet and wait for ACK (self.recv)
        """

        while True:
            # Exit condition: EOF
            if self.seq_num == len(self.packets): break

            # Send packet
            packet = self.packets[self.seq_num]
            self.monitor.send(self.recv_id, packet)
            if debug: log(f'Send Packet: {self.seq_num} (TO: {self.get_TO()})')
            
            # Wait for ACK
            self.recv(packet, debug=debug)
        
        # END
        packet = str.encode('END|', 'ascii')
        self.monitor.send(self.recv_id, packet)
        self.recv(packet, end=True)

        # Close the connection
        self.monitor.send_end(self.recv_id)

        log(f'Close the connection: {self.send_id}')


    def recv(self, packet, end=False, debug=False):
        """
        Wait for receiving ACK packet
        - Re-transmit when receiving unexpected ACK and timeout

        Parameters
        ----------
        packet : binary string
            packet (used for re-transmission in this function)
        """

        while True:
            try:
                addr, ACK_packet  = self.monitor.recv(self.packet_size)
                if debug: log(f'Receive ACK: {ACK_packet}')

                # Ongoing process: Check packet sequence number is correct
                if not end:
                    # Re-send packet due to unexpected ACK number
                    if int(ACK_packet.decode('ascii')) != self.seq_num:
                        self.monitor.send(self.recv_id, packet)
                        if debug: log(f'Incorreck ACK, Re-Send: {self.seq_num} (TO: {self.get_TO()})\n')
                        continue

                    # Increase packet sequence number
                    self.inc_seq_num()
                    if debug: log(f'Increase Seq Num: {self.seq_num}\n')

                # End of process: Check seq_num == 'END'
                else:
                    # Re-send packet due to unexpected ACK number
                    if ACK_packet.decode('ascii') != 'END':
                        self.monitor.send(self.recv_id, packet)
                        if debug: log(f'Incorreck ACK, Re-Send: {self.seq_num} (TO: {self.get_TO()})\n')
                        continue

                # Successfully received: Leave the while loop
                break

            # Timeout condition
            except SOCKET.timeout:
                if debug: log('Timeout')

                # Re-send packet due to timeout
                self.monitor.send(self.recv_id, packet)
                if debug: log(f'Re-Send Packet: {self.seq_num} (TO: {self.get_TO()})\n')

                continue

    def close_connection(self):
        """
        Deactivate system to avoid further re-Transmission
        """

        self.active = False

    def inc_seq_num(self):
        """
        Increase the latest packet sequence number (after receiving ACK packet)
        """

        self.seq_num += 1

    def get_seq_num(self):
        """
        Get latest packet sequence number
        """

        return self.seq_num

    def get_packets(self):
        """
        Get packets that are ready to be sent
        """

        return self.packets

    def get_TO(self):
        """
        Retrun the timeout value
        """

        return self.timeout


def main(monitor, config):
    print()
    log('Sender Alive')

    FILE = open(config.get('nodes', 'file_to_send'), 'r')

    # Calculate the header size
    recv_id     = int(config.get('receiver',    'id'))
    send_id     = int(config.get('sender',      'id'))
    size_packet = int(config.get('network',     'MAX_PACKET_SIZE'))
    size_header = len(f'{send_id} {recv_id}\n'.encode('ascii'))

    # Split file content into chunkgs for conducting packets
    packets = split_content(FILE, size_packet, size_header)

    system = System(monitor, config, packets, send_id, recv_id, size_packet)
    system.send(debug=False)


if __name__ == '__main__':
    """
    Parse Configuration File / Initialize Monitor by Configration File
    """

    config_path = SYS.argv[1]
    config = CONFIGPARSER.RawConfigParser(allow_no_value=True)
    config.read(config_path)

    monitor = Monitor(config_path, 'sender')

    main(monitor, config)