import socket
import time
import sys
import os
from typing import Tuple, List

# Config File
import configparser

# Emulator
NePort = None

class config:
	# Network
	def __init__(self, MAX_PACKET_SIZE: int, LINK_BANDWIDTH: int):
		self.MAX_PACKET_SIZE = MAX_PACKET_SIZE
		self.LINK_BANDWIDTH = LINK_BANDWIDTH


# ==========================================================================================================================================
# CONSTANTS AND HELPERS
# ==========================================================================================================================================

MAX_HEADER_OVERHEAD = 30


def format_packet(source_id: int, dest_id: int, content: bytes) -> bytes:
	""" Formats a packet with content to be sent from source_id to dest_id via the network emulator"""
	return f'{source_id} {dest_id}\n'.encode('ascii') + content


def unformat_packet(packet: bytes or tuple) -> Tuple[int, bytes]:
	""" Clears a packet of formatting. If a tuple is given, clears and returns the first element. Returns a tuple (source id, content) """
	if isinstance(packet, tuple):
		return unformat_packet(packet[0])

	# Attempt to split
	try:
		return int(packet.split(b'\n')[0].split(b' ')[0]), packet.split(b'\n', maxsplit=1)[1]
	except:
		# Failed to parse packet!
		import traceback
		traceback.print_exc()
		print(f'Invalid packet received:\n{packet.decode("ascii")}')
		return None, None


def log(LOG_FILE_PATH, message):
	""" Logs a message for the user """
	with open(LOG_FILE_PATH, 'a+') as f:
		f.write(f'{message}\n')

def receiver_id(LOG_FILE_PATH, message):
		"""
		Attempts to parse the receiver id from this message. Receiver id is the second integer in the first line of the packet
		:return: int Receiver id. -1 on failure.
		"""
		try:
			return int(message.split(b'\n')[0].split(b' ')[1])
		except:
			log(LOG_FILE_PATH, f'Error reading receiver ID from first line of packet.')
			print('Error reading receiver ID from first line of packet.')
			return None

def sender_id(LOG_FILE_PATH, message):
	"""
	Attempts to parse the sender id from this message. Sender id is the first integer in the first line of the packet.
	:return: int Sender id. -1 on failure.
	"""
	
	try:
		return int(message.split(b'\n')[0].split(b' ')[0])
	except:
		log(LOG_FILE_PATH, f'Error reading sender ID from first line of packet.')
		print('Error reading sender ID from first line of packet.')
		return None

# ==========================================================================================================================================
# Network Monitor Class
# ==========================================================================================================================================

class Monitor:
	"""
	Network Monitor class to send data to the network emulator. This is also responsible 
	for calculating and keeping track of network statistics for that sender.
	"""
	def __init__(self, configFile, config_heading):
		self.LOG_FILE_PATH = None
		self.Config = None
		self.id = None
		self.ne_addr = None
		self.addr = None
		self.file = None
		self.read_config_file(configFile, config_heading)

		self.socketfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socketfd.bind(self.addr)
		with open(self.LOG_FILE_PATH, 'w+') as f:
			f.write(f'{time.time()}\nId:{self.id} | Starting monitor on {self.addr}.\n\n')

		self.total_time = 0
		self.last_sent_time = None
		self.last_recv_time = None
		
		# Dictionaries to hold per sender/receiver byte information
		self.in_data = {self.addr[1]: 0}
		self.in_packets = {self.addr[1]: 0}
		self.out_data = {self.addr[1]: 0}
		self.out_packets = {self.addr[1]: 0}

	def read_config_file(self, path, heading):
		""" Reads the configuration file and sets parameters """
		global NePORT

		try:
			cfg = configparser.RawConfigParser(allow_no_value=True)
			cfg.read(path)
		except Exception as e:
			print(e)
			print("FAILED! Configuration file exception")
			sys.exit(1)

		# Emulator
		self.LOG_FILE_PATH = cfg.get(heading, "log_file")
		self.ne_addr = ('localhost', int(cfg.get("emulator", "port")))

		# Network
		MAX_PACKET_SIZE=int(cfg.get("network", "MAX_PACKET_SIZE"))
		LINK_BANDWIDTH=int(cfg.get("network", "LINK_BANDWIDTH"))

		self.id = int(cfg.get(heading, 'id'))
		self.addr = (cfg.get(heading, 'host'), int(cfg.get(heading, 'port')))
		self.file = cfg.get('nodes', 'file_to_send')

		self.Config = config(MAX_PACKET_SIZE, LINK_BANDWIDTH)

	def send(self, dest, data):
		"""
		Sends the data to the the specified address
		"""
		if not isinstance(dest, int):
			raise ValueError("Destination must be an integer")
		if not isinstance(data, bytes):
			raise ValueError("Data must be a byte string")

		if self.last_sent_time:
			self.total_time += time.time() - self.last_sent_time
		
		# Update the sent timestamp
		self.last_sent_time = time.time()
		
		if dest in self.out_data:
			self.out_data[dest] += len(data)
		else:
			self.out_data[dest] = len(data)
		
		if dest in self.out_packets:
			self.out_packets[dest] += 1
		else:
			self.out_packets[dest] = 1

		#snum = data.split(b'\n')[1].split()[0]
		#print(f'Sending seq num {snum}')
		self.socketfd.sendto(format_packet(self.id, dest, data), self.ne_addr)

	def recv(self, size):
		"""
		Returns the Tuple(sender ID, data) received at the socket.
		Data represents the message received in bytes. addr is the sender address.
		"""
		sender, data = unformat_packet(self.socketfd.recvfrom(size + MAX_HEADER_OVERHEAD))
		if sender is None:
			return None, None

		# print(f'Received {message} on id={self.id}')
		if sender in self.in_data:
			self.in_data[sender] += len(data)
		else:
			self.in_data[sender] = len(data)
		
		if sender in self.in_packets:
			self.in_packets[sender] += 1
		else:
			self.in_packets[sender] = 1
			
		return sender, data

	def send_end(self, dest_id):
		"""Signals the end of transmission of the file. Should be called after the last ACK receive.

		Args:
			file : Path to the file being transmitted.
		"""
		assert isinstance(dest_id, int), 'Please give an integer ID!'
		self.total_time += time.time() - self.last_sent_time
		filesize = os.path.getsize(self.file)
		
		log(self.LOG_FILE_PATH, f'File Size					: {filesize} bytes')
		log(self.LOG_FILE_PATH, f'Total Bytes Transmitted		: {self.out_data[dest_id]} bytes')
		log(self.LOG_FILE_PATH, f'Overhead					: {self.out_data[dest_id] - filesize} bytes')
		log(self.LOG_FILE_PATH, f'Number of Packets sent		: {self.out_packets[dest_id]}')
		log(self.LOG_FILE_PATH, f'Total Time					: {round(self.total_time, 2)} secs')
		log(self.LOG_FILE_PATH, f'Goodput					: {round(filesize/self.total_time, 2)} bytes/sec')

		# Reset the counters for next file
		self.total_time = 0
		self.last_sent_time = None
		self.last_recv_time = None
		self.out_data[dest_id] = 0
		self.socketfd.sendto(f'{0} {0}\n'.encode('ascii'), self.ne_addr)

	def recv_end(self, recvfile, sender_id):
		"""Signals the end of receive of the file. Should be called after the last ACK is sent.

		Args:
			file : Path to the file being transmitted.
		"""
		match = True
		if not os.path.exists(recvfile):
			match = False
		else:
			with open(self.file) as orig:
				with open(recvfile) as recv:
					lines1 = orig.readlines()
					lines2 = recv.readlines()
					if len(lines1) != len(lines2):
						log(self.LOG_FILE_PATH, f'Received file and original have differing number of lines.')
						match = False
					else:
						for idx in range(len(lines1)):
							if lines1[idx] != lines2[idx]:
								log(self.LOG_FILE_PATH, f'Received file doesn\'t match the original file. Mismatch on line {idx}')
								match = False

		log(self.LOG_FILE_PATH, f'File transmission correct	: {match}')
		log(self.LOG_FILE_PATH, f'Number of Packets Received	: {self.out_packets[sender_id]}')
		log(self.LOG_FILE_PATH, f'Total Bytes Transmitted		: {self.in_data[sender_id]}')
		log(self.LOG_FILE_PATH, f'Total Time					: {round(self.total_time, 2)} secs')
		
		# Reset the counters for next file
		self.total_time = 0
		self.last_sent_time = None
		self.last_recv_time = None
		self.in_data[sender_id] = 0