# Simple software defined network (SDN)

The project assignment is about implementing a simple software defined network (SDN) system consisting of switches and a controller using Python programming language and UDP sockets for communication. The project aims to familiarize students with the concept of SDN network, improve their understanding of routing algorithms, and give them experience in socket programming. The project provides a handout with a full project description and guidelines for running the code and submitting the project. The controller.py and switch.py codes need to be submitted without any binaries, and the git repo should only contain source files. The project requires supporting command line arguments, using K=2 and TIMEOUT=3*K, following the convention for printing logs, and not modifying the provided configuration files. Grading will be based on the test configurations provided with the starter code and some hidden tests, and students should ensure their code can handle all failure and restart scenarios for full points.

## Usage
> python controller.py [controller port] [config file]\
> python switch.py \<switchID> \<controller hostname> \<controller port> -f \<neighbor ID>

The Controller should be executed first in a separate terminal. While it is running each switch should be launched in a separate terminal with the Switch ID, Controller hostname and the port.

### Note:
1. You must support command line arguments in the above format. Note that the “-f” flag for the switch is a  parameter for link failures (See ‘Simulating Link Failure’), and we must be able to run your code with and without this flag.
2. Please use ```K = 2; TIMEOUT = 3* K``` (recall these parameters pertain to timers related to Periodic operations of the switch and the Controller)
3. As mentioned earlier, all logs that you print must strictly follow the convention described.
4. Do not modify the provided configuration files.