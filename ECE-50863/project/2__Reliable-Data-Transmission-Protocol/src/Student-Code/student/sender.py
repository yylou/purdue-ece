#!/usr/bin/env python3
#
#    Author : Yuan-Yao Lou (Mike) <yylou@purdue.edu>
#    Title  : Ph.D. student in ECE at Purdue University
#    Date   : 2021/10/21
#


from os import sync
from monitor import Monitor

import sys          as SYS
import configparser as CONFIGPARSER
import datetime     as DATETIME
import time         as TIME
import threading    as THREAD
import socket       as SOCKET


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
    Split file content into chunks for sending packets: <seq_num>: <data>

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


class System:
    """
    Sender System Information: Connection Status, Packet Sequence Number, Packet Record, Timeout
    """

    def __init__(self, monitor, config, packets, send_id, recv_id, size_packet, wnd_size):
        self.monitor        = monitor
        self.send_id        = send_id
        self.recv_id        = recv_id
        self.packet_size    = size_packet

        self.active         = True          # System is active (connected w/ receiver)
        self.wnd_size       = wnd_size      # wnd_size
        self.packets        = packets       # Packets ready to be sent; <seq_num>: <data>
        self.ack            = {seq_num: False for seq_num in packets}   # ACK record: <seq_num>: <True|False>
        
        # Calculate and set timeout value to Minitor
        timeout             = 1.65 * (int(config.get("network", "MAX_PACKET_SIZE")) / int(config.get("network", "LINK_BANDWIDTH")) + 2 * float(config.get("network", "PROP_DELAY")))
        self.timeout        = max(0.35, min(0.65, timeout))
        self.timeout        = 0.2
        self.monitor.socketfd.settimeout(self.timeout)

    def _send_wnd(self, base, end, debug=False):
        """
        v10.23

        Parameters
        ----------
        
        """
        
        end = end if end < len(self.packets) else len(self.packets)

        for seq_num in range(base, end):
            # Only resend unACKed packet
            if not self.ack[seq_num]: 
                self.monitor.send(self.recv_id, self.packets[seq_num])
                if debug: log(f'Send Packet: {seq_num}')

    def _send(self, debug=False):
        """
        v10.23

        Parameters
        ----------
        
        """

        # Initial Sending Process
        base, end = 0, 0 + self.wnd_size
        self._send_wnd(base, end, debug)

        while base < len(self.packets):
            try:
                addr, ACK_packet = self.monitor.recv(self.packet_size)
                seq_num = int(ACK_packet.decode('ascii'))

                # Normal ACK Message / Within Current Window
                if base <= seq_num < end:
                    if debug: log(f'Receive ACK: {seq_num}')

                    self.ack[seq_num] = True

                    # Packets in the current window are all ACKed / Move sliding window
                    if all([self.ack[_] for _ in range(base, end)]):
                        if debug: log(f'All ACKed for Current Window: {base}, {end}')

                        base += self.wnd_size
                        end  += self.wnd_size
                        end   = end if end < len(self.packets) else len(self.packets)
                        self._send_wnd(base, end, debug)

            except SOCKET.timeout:
                if debug: log('Re-Send Packets')
                self._send_wnd(base, end, debug)

        # END
        packet = str.encode('E|', 'ascii')
        self.monitor.send(self.recv_id, packet)
        while True:
            try:
                addr, ACK_packet = self.monitor.recv(self.packet_size)
                seq_num = ACK_packet.decode('ascii')

                if seq_num == 'E': break
                else: continue

            except SOCKET.timeout:
                self.monitor.send(self.recv_id, packet)

        # Close the connection
        self.monitor.send_end(self.recv_id)

        log(f'Close the connection: {self.send_id}')

    def send_wnd(self, base, debug=False):
        """
        v10.25

        Parameters
        ----------
        
        """
        
        end = min(len(self.packets), base + self.wnd_size)

        for seq_num in range(base, end):
            # Only resend unACKed packet
            if not self.ack[seq_num]: 
                if debug: log(f'Send Packet: {seq_num}')
                self.monitor.send(self.recv_id, self.packets[seq_num])

    def send(self, debug=False):
        """
        v10.25

        Parameters
        ----------
        
        """

        # ==================================================
        #   Initial Sending Process                        =
        # ==================================================
        base = 0
        self.send_wnd(base, debug)

        while base < len(self.packets):
            end = min(len(self.packets), base + self.wnd_size)
        
            try:
                addr, ACK_packet = self.monitor.recv(self.packet_size)
                seq_num = int(ACK_packet.decode('ascii'))

                # ==================================================
                #   Normal ACK Message / Within Current Window     =
                # ==================================================
                if base <= seq_num <= base + self.wnd_size:
                    if debug: log(f'Receive ACK: {seq_num}')
                    self.ack[seq_num] = True

                    expand  = seq_num - base + 1
                    new_end = min(len(self.packets), end + expand)

                    for seq_num in range(end, new_end):
                        if debug: log(f'Send Packet: {seq_num}')
                        self.monitor.send(self.recv_id, self.packets[seq_num])

                    # Debug purpose: Window Diagnosis
                    if debug: log(f'Expand: {expand}, Base: {base}, End: {end}, New End: {new_end}')
                    base += expand
                
                else:
                    if debug: log(f'Receive ACK: {seq_num}')
                    self.ack[seq_num] = True

            except SOCKET.timeout:
                if debug: log(f'Re-Send Packets')
                self.send_wnd(base, debug)
                if debug: log( '---------------')

        # ==================================================
        #   Check for unACKed packts                       =
        # ==================================================
        while not all(self.ack.values()):
            done = False
            unACKed = set([str(_) for _ in self.ack.keys() if not self.ack[_]])
            if debug: log(f'[Before] unACKed Packets (Sender): {unACKed}')

            while True:
                # ==================================================
                #   Send unACKed Confirmation                      =
                # ==================================================
                packet = str.encode(f'C|{"|".join(unACKed)}', 'ascii')
                self.monitor.send(self.recv_id, packet)

                try:
                    addr, packet = self.monitor.recv(self.packet_size)
                    if debug: log(f'unACKed Packet (from Receiver): {packet}')
                    packet = set(packet.decode('ascii').split('|'))
                    
                    # Receiver confirms all packets are ACKed
                    if len(packet) == 1 and list(packet)[0] == '':
                        done = True
                        break
                    
                    unACKed_tmp = set([int(_) for _ in packet])
                    unACKed     = set([int(_) for _ in unACKed]) - unACKed_tmp
                    for seq_num in unACKed: self.ack[seq_num] = True
                    unACKed = sorted(unACKed_tmp)
                    
                    if debug: log(f'[After]  unACKed Packets (Sender): {unACKed}')
                    break

                except SOCKET.timeout:
                    if debug: log(f'Timeout, Resend Confirmation Packet')
                    continue

            if done: break

            # ==================================================
            #   Send unACKed packts                            =
            # ==================================================
            for seq_num in unACKed:
                if debug: log(f'Send Packet: {seq_num}')
                self.monitor.send(self.recv_id, self.packets[int(seq_num)])

            while not all(self.ack.values()):
                try:
                    addr, ACK_packet = self.monitor.recv(self.packet_size)
                    if debug: log(f'Receive ACK: {ACK_packet}')
                    
                    # Unexpected packet due to re-ordering
                    ACK_packet = ACK_packet.decode('ascii')
                    if not ACK_packet.isdigit(): continue

                    seq_num = int(ACK_packet)
                    self.ack[seq_num] = True

                except SOCKET.timeout:
                    if debug: log(f'Timeout, Back to check unACKed Packet')
                    break

        # ==================================================
        #   END                                            =
        # ==================================================
        packet = str.encode('E|', 'ascii')
        self.monitor.send(self.recv_id, packet)
        if debug: log(f'Send Packet: END')
        while True:
            try:
                addr, ACK_packet = self.monitor.recv(self.packet_size)
                seq_num = ACK_packet.decode('ascii')

                if seq_num == 'E': break

            except SOCKET.timeout:
                self.monitor.send(self.recv_id, packet)

        # Sanity (unACKed) Check
        if debug:
            unACKed = [_ for _ in self.ack.keys() if not self.ack[_]]
            print(); log(f'unACKed Packets (#{len(unACKed)} / {len(self.packets)}): {unACKed}')

        # Close the connection
        self.monitor.send_end(self.recv_id)
        log(f'Close the connection: {self.send_id}')

    def send_packet(self, debug=False):
        """
        v11.02

        Parameters
        ----------
        
        """

        # ==================================================
        #   Initial Sending Process                        =
        # ==================================================
        base = 0
        self.send_wnd(base, debug)

        sync_record = {}

        while base < len(self.packets) or sync_record:
            end = min(len(self.packets), base + self.wnd_size)
        
            try:
                addr, ACK_packet = self.monitor.recv(self.packet_size)
                seq_num = ACK_packet.decode('ascii')

                # ==================================================
                #   Receive Sync Message                           =
                # ==================================================
                if seq_num.count('|') > 1:
                    if debug: log(f'Receive Sync Packet: {seq_num}')

                    key, data = seq_num.split('||')
                    req = set(map(int, key[2:].split('|')))

                    if data: 
                        ans = set(map(int, data.split('|')))

                    else: 
                        ans = set()
                        if key in sync_record: 
                            if debug: log(f'Sync Record: {sync_record.keys()}')
                            if debug: log(f'Delete Sync Record: {key}')
                            del sync_record[key]

                    for element in req:
                        if element not in ans: self.ack[element] = True
                        else: 
                            if debug: log(f'Send Packet (from Sync): {element}')
                            self.monitor.send(self.recv_id, self.packets[element])

                            if key in sync_record: del sync_record[key]
                            sync_record[f'S|{element}'] = DATETIME.datetime.now()

                    if debug: log(f'Sync Record: {sync_record}')

                # ==================================================
                #   Normal ACK Message / Within Current Window     =
                # ==================================================
                else:
                    seq_num = int(ACK_packet.decode('ascii'))

                    # ==================================================
                    #   Review Sync Message                            =
                    # ==================================================
                    timer = DATETIME.datetime.now()
                    if sync_record:
                        for msg in sync_record:
                            if timer - sync_record[msg] > DATETIME.timedelta(microseconds=500000):
                                if debug: log(f'Sync Record: {sync_record}')
                                if debug: log(f'Review Sync Packet: {msg}, Elapsed Time: {(timer - sync_record[msg]).microseconds}')
                                self.monitor.send(self.recv_id, str.encode(msg, 'ascii'))

                                sync_record[msg] = DATETIME.datetime.now()

                    if base <= seq_num <= base + self.wnd_size:
                        if debug: log(f'Receive ACK: {seq_num}')
                        self.ack[seq_num] = True

                        expand  = seq_num - base + 1
                        new_end = min(len(self.packets), end + expand)

                        # ==================================================
                        #   Send Sync Packet                               =
                        # ==================================================
                        if expand > 1:
                            gap = [str(_) for _ in range(base, base + expand - 1)]
                            content = f'S|{"|".join(gap)}'
                            packet = str.encode(f'{content}', 'ascii')
                            
                            if debug: log(f'Send Sync Packet: {packet}')
                            self.monitor.send(self.recv_id, packet)

                            sync_record[content] = DATETIME.datetime.now()
                            if debug: log(f'Sync Record: {sync_record}')

                        # ==================================================
                        #   Send Normal Packet                             =
                        # ==================================================
                        for seq_num in range(end, new_end):
                            if debug: log(f'Send Packet: {seq_num}')
                            self.monitor.send(self.recv_id, self.packets[seq_num])

                        # Debug purpose: Window Diagnosis
                        if debug: log(f'Expand: {expand}, Base: {base}, End: {end}, New End: {new_end}')
                        base += expand
                    
                    else:
                        if debug: log(f'Receive ACK: {seq_num}')
                        self.ack[seq_num] = True

                        # ==================================================
                        #   Review Sync Message                            =
                        # ==================================================
                        remove = set()
                        for element in sync_record:
                            if element[2:].isdigit() and int(element[2:]) == seq_num: remove.add(element)
                        if debug and remove: 
                            log(f'Sync Record: {sync_record.keys()}')
                            log(f'Remove Sync Record: {remove}')
                        for element in remove:
                            if element in sync_record: 
                                del sync_record[element]
                        if debug and remove: 
                            log(f'Sync Record: {sync_record.keys()}')

            except SOCKET.timeout:
                if debug: log(f'===  Timeout  ===')

                # If any Sync record remains
                if sync_record:
                    for element in sync_record:
                        self.monitor.send(self.recv_id, str.encode(element, 'ascii'))
                        if debug: log(f'Re-Send Sync Packet: {element}')

                # Error Handling
                if base > 0 and not all(self.ack.values()):
                    unACK = []
                    for seq_num in self.ack:
                        if not self.ack[seq_num]: self.monitor.send(self.recv_id, self.packets[seq_num])
                    
                if debug: log( '=================')

        # ==================================================
        #   END                                            =
        # ==================================================
        packet = str.encode('E|', 'ascii')
        self.monitor.send(self.recv_id, packet)
        if debug: log(f'Send Packet: END')
        while True:
            try:
                addr, ACK_packet = self.monitor.recv(self.packet_size)
                seq_num = ACK_packet.decode('ascii')

                if seq_num == 'E': break

            except SOCKET.timeout:
                self.monitor.send(self.recv_id, packet)

        # Sanity (unACKed) Check
        if debug:
            unACKed = [_ for _ in self.ack.keys() if not self.ack[_]]
            print(); log(f'unACKed Packets (#{len(unACKed)} / {len(self.packets)}): {unACKed}')
            print(); log(f'{sync_record}')

        # Close the connection
        self.monitor.send_end(self.recv_id)
        log(f'Close the connection: {self.send_id}')

    def close_connection(self):
        """
        Deactivate system to avoid further re-Transmission
        """

        self.active = False

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

    system = System(monitor, config, packets, send_id, recv_id, size_packet, int(config.get('sender', 'window_size')))
    system.send_packet(debug=False)


if __name__ == '__main__':
    """
    Parse Configuration File / Initialize Monitor by Configration File
    """

    config_path = SYS.argv[1]
    config = CONFIGPARSER.RawConfigParser(allow_no_value=True)
    config.read(config_path)

    monitor = Monitor(config_path, 'sender')

    main(monitor, config)