# Python
PYTHON = python3

# Paths to student scripts
SENDER_PATH = "./sender.py"
RECEIVER_PATH = "./receiver.py"

# Ports to clear
# These ports are currently hardcoded in the config file. 
# If you modify the ports in config file they should be changed here as well. 
SENDER_PORT = 8001
RECEIVER_PORT = 8002

# Runs the sender
run-sender:
	-kill -9 $$(lsof -t -i:$(SENDER_PORT))
	$(PYTHON) $(SENDER_PATH) "$(config)"

# Runs the receiver
run-receiver:
	-kill -9 $$(lsof -t -i:$(RECEIVER_PORT))
	$(PYTHON) $(RECEIVER_PATH) "$(config)"
