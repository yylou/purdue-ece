#!/usr/bin/env python3
from monitor import Monitor
import sys

# Config File
import configparser

if __name__ == '__main__':
	print("Sender starting up!")
	config_path = sys.argv[1]

	# Initialize sender monitor
	send_monitor = Monitor(config_path, 'sender')
	
	# Parse config file
	cfg = configparser.RawConfigParser(allow_no_value=True)
	cfg.read(config_path)
	receiver_id = int(cfg.get('receiver', 'id'))
	file_to_send = cfg.get('nodes', 'file_to_send')
	max_packet_size = int(cfg.get('network', 'MAX_PACKET_SIZE'))

	# Exchange messages!
	print('Sender: Sending "Hello, World!" to receiver.')
	send_monitor.send(receiver_id, b'Hello, World!')
	addr, data = send_monitor.recv(max_packet_size)
	print(f'Sender: Got response from id {addr}: {data}')

	# Exit! Make sure the receiver ends before the sender. send_end will stop the emulator.
	send_monitor.send_end(receiver_id)