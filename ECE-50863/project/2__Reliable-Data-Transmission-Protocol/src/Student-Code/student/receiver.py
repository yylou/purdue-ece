#!/usr/bin/env python3
#
#    Author : Yuan-Yao Lou (Mike) <yylou@purdue.edu>
#    Title  : Ph.D. student in ECE at Purdue University
#    Date   : 2021/10/21
#


from monitor import Monitor

import sys as SYS
import configparser as CONFIGPARSER
import datetime as DATETIME
import time as TIME
import threading as THREAD


def log(msg):
    """
    Function
    ----------
    System Log Information

    Parameters
    ----------
    msg : str
        message for logging purpose
    """
    
    print('{0:<30} |{1:<5}{2}'.format(str(DATETIME.datetime.now()), ' ', msg))


class System():
    """
    Receiver System Information: Connection Status, Packet Sequence Number, Packet Record
    """

    def __init__(self, monitor, config):
        self.monitor        = monitor
        self.recv_id        = int(config.get('receiver',    'id'))
        self.send_id        = int(config.get('sender',      'id'))
        self.packet_size    = int(config.get('network',     'MAX_PACKET_SIZE'))

        self.active         = True      # System is active (in connection w/ sender)
        self.packet_record  = {}        # Packet record; <seq_num>: <data>

        self.FILE_NAME      = config.get('receiver', 'write_location')

    def recv(self, debug=False):
        """
        v10.25

        Parameters
        ----------
        
        """

        while True:
            # Receive packet / Split packet content by '|' with maxsplit=1
            addr, packet = self.monitor.recv(self.packet_size)
            packet  = packet.split('|'.encode('ascii'), maxsplit=1)
            seq_num = packet[0].decode('ascii')
            data    = packet[1]
            if debug: log(f'Receive Packet: {seq_num}')

            # ==================================================
            #   EOF                                            =
            # ==================================================
            if seq_num == 'E':
                self.monitor.send(self.send_id, str.encode('E', 'ascii'))
                if debug: log(f'Send ACK: {seq_num}')

                if self.get_connection_status():
                    # Write to File before 'recvend'
                    with open(self.FILE_NAME, 'wb') as FILE:
                        for id in sorted(self.packet_record.keys()):
                            FILE.write(self.packet_record[id])

                    # Close the connection
                    self.monitor.recv_end(self.FILE_NAME, self.send_id)
                    self.close_connection()

                    log(f'Close the connection: {self.recv_id}')

                    # Sanity (unACKed) Check
                    if debug:
                        ACKed = [_ for _ in self.packet_record.keys()]
                        print(); log(f'ACKed Packets (#{len(ACKed)}): {sorted(ACKed)}')

                # TODO: NEED TO COMMENT FOR DEPLOYMENT
                if not self.get_connection_status(): break

            # ==================================================
            #   unACKed Confirmation                           =
            # ==================================================
            elif seq_num == 'C':
                unACKed = []
                data = data.decode('ascii').split('|')
                for element in data: 
                    if int(element) not in self.packet_record: unACKed.append(element)

                if debug: log(f'unACKed Packet (Receiver): {unACKed}')

                self.monitor.send(self.send_id, str.encode(f'{"|".join(unACKed)}', 'ascii'))

            # ==================================================
            #   Send ACK                                       =
            # ==================================================
            else:
                
                self.monitor.send(self.send_id, str.encode(f'{seq_num}', 'ascii'))
                if debug: log(f'Send ACK: {seq_num}')

                # Update packet record
                seq_num = int(seq_num)
                self.update_packet_record(seq_num, data)

    def recv_packet(self, debug=False):
        """
        v11.02

        Parameters
        ----------
        
        """

        while True:
            # Receive packet / Split packet content by '|' with maxsplit=1
            addr, packet = self.monitor.recv(self.packet_size)
            packet  = packet.split('|'.encode('ascii'), maxsplit=1)
            seq_num = packet[0].decode('ascii')
            data    = packet[1]
            if debug: log(f'Receive Packet: {seq_num}')

            # ==================================================
            #   EOF                                            =
            # ==================================================
            if seq_num == 'E':
                self.monitor.send(self.send_id, str.encode('E', 'ascii'))
                if debug: log(f'Send ACK: {seq_num}')

                if self.get_connection_status():
                    # Write to File before 'recvend'
                    with open(self.FILE_NAME, 'wb') as FILE:
                        for id in sorted(self.packet_record.keys()):
                            FILE.write(self.packet_record[id])

                    # Close the connection
                    self.monitor.recv_end(self.FILE_NAME, self.send_id)
                    self.close_connection()

                    log(f'Close the connection: {self.recv_id}')

                    # Sanity (unACKed) Check
                    if debug:
                        ACKed = [_ for _ in self.packet_record.keys()]
                        print(); log(f'ACKed Packets (#{len(ACKed)}): {sorted(ACKed)}')

                # TODO: NEED TO COMMENT FOR DEPLOYMENT
                # if not self.get_connection_status(): break

            # ==================================================
            #   unACKed Confirmation                           =
            # ==================================================
            elif seq_num == 'C':
                unACKed = []
                data = data.decode('ascii').split('|')
                for element in data: 
                    if int(element) not in self.packet_record: unACKed.append(element)

                if debug: log(f'unACKed Packet (Receiver): {unACKed}')
                self.monitor.send(self.send_id, str.encode(f'{"|".join(unACKed)}', 'ascii'))

            # ==================================================
            #   Sync Message                                   =
            # ==================================================
            elif seq_num == 'S':
                if debug: log(f'Receive Sync Packet: {seq_num}|{data}')

                data = data.decode('ascii')
                packet = f'{seq_num}|{data}'
                data = data.split('|')

                unACKed = []
                for element in data: 
                    if int(element) not in self.packet_record: unACKed.append(element)

                packet = str.encode(f'{packet}||{"|".join(unACKed)}', 'ascii')

                if debug: log(f'Send Sync Packet: {packet}')
                self.monitor.send(self.send_id, packet)

            # ==================================================
            #   Send ACK                                       =
            # ==================================================
            else:
                self.monitor.send(self.send_id, str.encode(f'{seq_num}', 'ascii'))
                if debug: log(f'Send ACK: {seq_num}')

                # Update packet record
                seq_num = int(seq_num)
                self.update_packet_record(seq_num, data)
                
                # Verify gap 
                if debug:
                    gap = []
                    for i in range(0, max(self.packet_record.keys())):
                        if i not in self.packet_record: gap.append(i)
                    log(f'Gap: {gap}')

    def close_connection(self):
        """
        Deactivate system to avoid calling recv_end multiple times
        """

        self.active = False

    def update_packet_record(self, seq_num, data):
        """
        Add data into packet record

        Parameters
        ----------
        seq_num : int
            packet sequence number

        data : str
            packet data
        """

        self.packet_record[seq_num] = data

    def get_connection_status(self):
        """
        Get connection status (to avoid calling recv_end multiple times due to final ACK dropped)
        """

        return self.active


def main(monitor, config):
    print()
    log('Receiver Alive')

    system = System(monitor, config)
    system.recv_packet(debug=False)


if __name__ == '__main__':
    """
    Parse Configuration File / Initialize Monitor by Configration File
    """

    config_path = SYS.argv[1]
    config = CONFIGPARSER.RawConfigParser(allow_no_value=True)
    config.read(config_path)

    monitor = Monitor(config_path, 'receiver')

    main(monitor, config)