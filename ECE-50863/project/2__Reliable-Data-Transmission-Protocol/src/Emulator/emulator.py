#!/usr/bin/env python
from threading import Thread
import socket
import time
import sys
import os
from typing import Tuple

# Config File
import configparser
import io

# Probability Distibutions
import math
import random

# ==========================================================================================================================================
# DEBUG
# ==========================================================================================================================================


def packet_to_seq_num(packet):
	""" FOR DEBUGGING TA CODE. """
	return int(packet.data.split(b'\n')[1].split()[0])

# ==========================================================================================================================================
# CONFIGURATION LEVEL PARAMETERS
# ==========================================================================================================================================

SEND_SUCCESS = 1
SEND_FAIL = -1
PACKET_FAIL = -1
STAT_INTERVAL = 5

class node:
	""" Dataclass to hold node-specific information """
	def __init__(self, id: int, address: Tuple[str, int]):
		self.id = id # int
		self.address = address # Tuple[str, int]

class config:
	def __init__(self):
		# Latency queue
		self.PROP_DELAY: float = 1 # in millisecs
		# Sending queue
		self.MAX_PACKET_SIZE: int = 1024
		self.LINK_BANDWIDTH: int = 1024 # Bytes per second
		self.MAX_PACKETS_QUEUED: int = 1000 # Based on bandwidth restrictions ONLY. TODO: Return SEND_FAIL on error
		self.DROP_MODEL: int = 1 # Decides whether the drops are definite or dynamic
		self.RANDOM_DROP_PROBABILITY: float = 0
		self.REORDER_PROBABILITY: float = 0

# Emulator
LOG_FILE_PATH = './emulator.log'
HOST = ''
PORT = '8001'
nodes = None		# Dictionary to store the node information indexed by id
Config = None	   # Holds all the configuration information

def read_config_file(path):
	""" Reads the configuration file and sets parameters """
	global LOG_FILE_PATH
	global PORT
	global nodes
	global Config

	try:
		cfg = configparser.RawConfigParser(allow_no_value=True)
		cfg.read(path)
	except Exception as e:
		print(e)
		print("FAILED! Configuration file exception")
		sys.exit(1)

	# Emulator
	LOG_FILE_PATH = cfg.get("emulator", "log_file")
	PORT = int(cfg.get("emulator", "port"))

	# Network
	Config = config()
	Config.PROP_DELAY=float(cfg.get("network", "PROP_DELAY"))
	Config.MAX_PACKET_SIZE=int(cfg.get("network", "MAX_PACKET_SIZE"))
	Config.LINK_BANDWIDTH=int(cfg.get("network", "LINK_BANDWIDTH"))
	Config.DROP_MODEL=int(cfg.get("network", "DROP_MODEL"))
	Config.RANDOM_DROP_PROBABILITY=float(cfg.get("network", "RANDOM_DROP_PROBABILITY"))
	Config.REORDER_PROBABILITY=float(cfg.get("network", "REORDER_PROBABILITY"))
	Config.MAX_PACKETS_QUEUED= int(2*Config.PROP_DELAY*(Config.LINK_BANDWIDTH/Config.MAX_PACKET_SIZE)) + 1 # The bandwidth delay product

	print("Config Parsed: ", Config)

	# Nodes
	node_headers = cfg.get("nodes", "config_headers").split(',')
	nodes = {}
	for header in node_headers:
		id = int(cfg.get(header, 'id'))
		host = cfg.get(header, "host")
		port = int(cfg.get(header, "port"))
		nodes[id] = node(id, (host, port))
	
	# print("Log file : ", LOG_FILE_PATH)
	with open(LOG_FILE_PATH, 'w+') as f:
		f.write(f'{time.time()}\n{"Configuration File Parsed."}\n')


# ==========================================================================================================================================
# CONSTANTS AND HELPERS
# ==========================================================================================================================================

def log(message):
	""" Logs a message for the user """
	with open(LOG_FILE_PATH, 'a+') as f:
		f.write(f'{time.time()}\n{message}\n\n')

class Packet:
	"""
	Holds the data and sender address for a single packet. Also records the time when it should be dequeued from the latency queue.
	Packets are expected to have a header <sender ID> <receiver ID> in their first line
	"""
	def __init__(self, data, addr):
		self.data = data
		self.addr = addr	# Sender(Node) Address
		self.timestamp = time.time()
		self.latency_complete_time = self.timestamp + Config.PROP_DELAY

	def sender_id(self):
		"""
		Attempts to parse the sender id from this packet. Sender id is the first integer in the first line of the packet.
		:return: int Sender id. -1 on failure.
		"""
		try:
			return int(self.data.split(b'\n')[0].split(b' ')[0])
		except:
			log(f'Error reading sender ID from first line of packet.')
			print('Error reading sender ID from first line of packet.')
			return PACKET_FAIL

	def receiver_id(self):
		"""
		Attempts to parse the receiver id from this packet. Receiver id is the second integer in the first line of the packet
		:return: int Receiver id. -1 on failure.
		"""
		try:
			return int(self.data.split(b'\n')[0].split(b' ')[1])
		except:
			log(f'Error reading receiver ID from first line of packet.')
			print('Error reading receiver ID from first line of packet.')
			return PACKET_FAIL


# ==========================================================================================================================================
# LATENCY QUEUE AND SENDING BUFFER
# ==========================================================================================================================================

class LatencyQueue:
	"""
	Latency queue handles the receipt of messages in a new thread. Functions are ATOMIC. Returns received messages in order when their
	latency is complete.

	Latency queue is deterministic and only used to simulate wire latency. Does not impose any other constraints.
	"""
	def __init__(self, socketfd):
		self._queue = []
		self._sockfd = socketfd

		# Start the incoming traffic count
		self._in_traffic = 0.0
		self._total_bytes = 0.0
		self._start_time = time.time()
		self._last_recved = time.time()
		
		# Terminate Flag
		self.terminate = False

		# Start the receive thread.
		th = Thread(target=lambda: self._recv_thread())
		th.setDaemon(True)
		th.start()

	def _recv_thread(self):
		""" Polls the UDP socket and enqueues packets in the latency queue"""
		while True:
			try:
				data, addr = self._sockfd.recvfrom(Config.MAX_PACKET_SIZE)

				packet = Packet(data, addr)
				#print(f'Received #{packet_to_seq_num(packet)} -> {packet.receiver_id()}')

				if packet.receiver_id() == 0:
					log(f'Test Complete. Terminating...')
					self.terminate = True
					sys.exit()

				if time.time() > self._last_recved:
					self._in_traffic = len(data) / (time.time() - self._last_recved)
					self._last_recved = time.time()
					# print(f'Incoming Traffic: {self._in_traffic}  bytes/sec')

				# drop_count = max(0, len(self._queue) + 1 - Config.MAX_PACKETS_QUEUED)
				# self._queue = self._queue[:Config.MAX_PACKETS_QUEUED]
				# if drop_count:
				# 	log(f'Dropped {drop_count} packet{"s" if drop_count > 1 else ""} due to full buffer.')
				if packet.receiver_id() != PACKET_FAIL:		# Only admit packets with valid destinations
					self._queue.append(packet)
					self._total_bytes += len(data)
			except Exception as e:
				print('PROBLEM')
				import traceback
				traceback.print_exc()
	
	def get_avg_traffic(self):
		"""Returns the average incoming traffic to the latency queue
		and by extension the network emulator itself.
		"""
		return self._total_bytes/(time.time() - self._start_time)

	def get_ready_packets(self):
		"""
		Returns the packets that have completed their latency.
		Returns packets OUT OF ORDER-- if latency is variable, the packets are injected to sending buffer out of order
		:return: List of packets ready
		"""
		ready = []
		idx = 0
		curtime = time.time()
		while idx < len(self._queue):
			if self._queue[idx].latency_complete_time < curtime:
				packet = self._queue[idx]
				#print(f'Latency done for #{packet_to_seq_num(packet)} -> {packet.receiver_id()}')
				ready.append(self._queue.pop(idx))
			else:
				idx += 1
		return ready


class SendingQueue:
	"""
	Handles the sending of packets. Imposes the following:
		Bandwidth limitations
		Dropping
		Reordering
	"""
	def __init__(self, socketfd):
		self._queue = []
		self._queuesize = 0
		self._sockfd = socketfd
		self._bandwidth_counter = 0
		self._bandwidth_counter_update_time = time.time()

	def check_for_available_bandwidth(self):
		""" Returns True if bandwidth is available. Updates bandwidth counter. """
		self._bandwidth_counter -= Config.LINK_BANDWIDTH * (time.time() - self._bandwidth_counter_update_time)
		self._bandwidth_counter_update_time = time.time()
		self._bandwidth_counter = max(self._bandwidth_counter, -100)
		# time.sleep(1/Config.LINK_BANDWIDTH)
		return self._bandwidth_counter <= 0

	def get_next_packet(self):
		"""
		Selects the next packet to dequeue. Imposes bandwidth restrictions, reordering, dropping
		:return: Packet, or None if no packet to send
		"""
		if not self.check_for_available_bandwidth():
			return
		
		if not self._queue:
			return None

		next_packet = None
		packet_drop = False

		while self._queue and not next_packet:
			next_packet = self._queue.pop(0)	# In-order Queue

			# if b'ACK' in next_packet.data:
			# 	print('ACK found!\n')

			if self.drop():
				# If the packet is dropped then try again
				log(f'Dropped Packet from {next_packet.addr}')
				print(f'Dropped Packet from {next_packet.addr}')
				next_packet = None
				continue
			
			if len(self._queue) > 1 and self.reorder():
				self._queue.insert(random.randint(1, min(len(self._queue)-1, 6)), next_packet)
				log(f'Reordered Packet from {next_packet.addr} to index {self._queue.index(next_packet)}')
				print(f'Redordered Packet from {next_packet.addr} to index {self._queue.index(next_packet)}')
				next_packet = None
				continue

		if next_packet is not None:
			self._bandwidth_counter += len(next_packet.data)
			self._queuesize -= len(next_packet.data)
			#debugprint = 'Bstatus:'
			#for dest in set(p.receiver_id() for p in self._queue):
			#	debugprint += f'\n\t->{dest}: ' + ', '.join(str(packet_to_seq_num(p)) for p in self._queue if p.receiver_id() == dest)
			#print(debugprint)

		return next_packet

	def drop(self):
		"""
		Decides if the next packet should be dropped with the given probability
		"""
		# For dynamic drop based on queue size
		if Config.DROP_MODEL == 2:
			mean = 2*(Config.PROP_DELAY + Config.MAX_PACKET_SIZE/Config.LINK_BANDWIDTH)*Config.LINK_BANDWIDTH
			if random.gauss(mean, mean/3) < self._queuesize:
				# Get a random sample from Normal Distribution.
				# This is based on how full the current queue is.
				return True
		
		elif Config.DROP_MODEL == 1 and random.uniform(0, 1) < Config.RANDOM_DROP_PROBABILITY < 1:
			return True
		
		else:
			return False

	def reorder(self):
		"""
		Decides if the next packet should be reordered with the given probability
		"""
		if random.uniform(0, 1) < Config.REORDER_PROBABILITY < 1:
			return True
		
		else:
			return False

	def add(self, packets):
		"""
		Receives packets from the sending queue and enqueues them
		:param packets: Packet(s) to receive
		"""
		if isinstance(packets, Packet):
			self.add([packets])
			return
		for packet in packets:
			drop_count = max(0, len(self._queue) + 1 - Config.MAX_PACKETS_QUEUED)
			self._queue = self._queue[:Config.MAX_PACKETS_QUEUED]
			if drop_count > 0:
				log(f'Dropped {drop_count} packet{"s" if drop_count > 1 else ""} for {packet.receiver_id()} due to full buffer.')
				print(f'Dropped {drop_count} packet{"s" if drop_count > 1 else ""} for {packet.receiver_id()} due to full buffer.')
			elif packet.receiver_id() != PACKET_FAIL:		# Only admit packets with valid destinations
				self._queue.append(packet)
				self._queuesize += len(packet.data)



# ==========================================================================================================================================
# NETWORK EMULATOR
# ==========================================================================================================================================

class NetworkEmulator:
	"""
	Network emulator class initializes a Latency Queue and a Sending Buffer on one port. Completes bootstrap sequence with
	clients, then sends packets as they make it through the queue/buffer.
	"""
	def __init__(self, host, port, num_NODES):
		log(f'Starting network emulator on {host} {port}.')
		self.socketfd = None
		self.client_addresses = {}
		self._stat_time = time.time()

		self.bootstrap(host, port)

		self.terminate = False
		self.latency_queue = LatencyQueue(self.socketfd)
		self.sending_buffers = {}

	def bootstrap(self, host, port):
		"""
		Engages in the boostrap sequence. 
		:param host: str Host for this NE's socket
		:param port: str Port for this NE's socket
		"""
		self.socketfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socketfd.bind((host, port))
		print("Network Emulator is up and running.")

	def get_dest_address(self, packet):
		"""
		Parses the destination address from this packet and this emulator's saved client addresses.
		:param packet: Packet to check
		:return: (host, port) of destination
		"""
		dest = packet.receiver_id()
		if not dest:
			return None
		elif dest not in nodes:
			log(f'Parsed destination id {dest} does not have a known address.')
			return None
		else:
			return nodes[dest].address

	def enqueue_sending(self, packet):
		"""
		Enqueues a packet in the proper sending queue
		:param packet: Packet to enqueue
		"""
		dest = packet.receiver_id()
		if dest is None:
			return
		if dest not in self.sending_buffers:
			self.sending_buffers[dest] = SendingQueue(self.socketfd)
		self.sending_buffers[dest].add(packet)

	def run(self):
		"""
		Infinite loop moves packets from the latency queue to the sending buffer, then sends ready packets from the sending buffer
		"""
		while not self.terminate:
			if self.latency_queue.terminate:
				sys.exit()

			for p in self.latency_queue.get_ready_packets():
				self.enqueue_sending(p)

			for dest, buffer in self.sending_buffers.items():
				to_send = buffer.get_next_packet()
				if to_send:
					addr = self.get_dest_address(to_send)
					if addr is not None:
						#print(f'Sending packet {packet_to_seq_num(to_send)} to id {dest}')
						self.socketfd.sendto(to_send.data, addr)
			
			if (self._stat_time + STAT_INTERVAL) < time.time():
				print(f'Current Average Incoming Traffic: {self.latency_queue.get_avg_traffic()} bytes/sec')
				log(f'Current Average Incoming Traffic: {self.latency_queue.get_avg_traffic()} bytes/sec')
				self._stat_time = time.time()


# ==========================================================================================================================================
# MAIN FUNCTION
# ==========================================================================================================================================


if __name__ == '__main__':
	print("Starting Network Emulator ...")
	assert len(sys.argv) == 2, 'Usage: python3 emulator.py <config_file_path>'
	read_config_file(sys.argv[1])

	ne = NetworkEmulator(host=HOST, port=PORT, num_NODES=len(nodes))
	ne.run()
