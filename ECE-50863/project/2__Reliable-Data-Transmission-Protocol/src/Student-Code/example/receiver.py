#!/usr/bin/env python3
from monitor import Monitor
import sys

# Config File
import configparser

if __name__ == '__main__':
	print("Receivier starting up!")
	config_path = sys.argv[1]

	# Initialize sender monitor
	recv_monitor = Monitor(config_path, 'receiver')
	
	# Parse config file
	cfg = configparser.RawConfigParser(allow_no_value=True)
	cfg.read(config_path)
	sender_id = int(cfg.get('sender', 'id'))
	file_to_send = cfg.get('nodes', 'file_to_send')
	max_packet_size = int(cfg.get('network', 'MAX_PACKET_SIZE'))

	# Exchange messages!
	addr, data = recv_monitor.recv(max_packet_size)
	print(f'Receiver: Got message from id {addr}: {data}')
	print('Receiver: Responding with "Hello, Sender!".')
	recv_monitor.send(sender_id, b'Hello, Sender!')

	# Exit! Make sure the receiver ends before the sender. send_end will stop the emulator.
	recv_monitor.recv_end('received_file', sender_id)