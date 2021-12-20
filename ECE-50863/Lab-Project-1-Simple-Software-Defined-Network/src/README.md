# Project I: Building a simple software defined network (SDN)

In this project, you will implement a highly simplified SDN system comprising a set of switches and a controller implemented as user level python processes. The process mimic the switches and controller, bind to distinct UDP ports, and communicate using UDP sockets. The project will (i) expose you to the concept of an SDN network; (ii) improve your understanding of routing algorithms; and (iii) give you experience with socket programming. 

Please refer to the course pages for the project handout which has the full project description. Below, we summarize key items related to running your code for your convenience. We also provide the procedure for submitting your code.


## Running your code and Important Requirements
We must be able to an run the Controller and Switch python files by running:

> python controller.py [controller port] [config file]\
> python switch.py \<switchID> \<controller hostname> \<controller port> -f \<neighbor ID>

The Controller should be executed first in a separate terminal. While it is running each switch should be launched in a separate terminal with the Switch ID, Controller hostname and the port.

### Important Requirements:
To be compatible with the auto-grader, the following are mandatory requirements:
1. You must support command line arguments in the above format. Note that the “-f” flag for the switch is a  parameter for link failures (See ‘Simulating Link Failure’), and we must be able to run your code with and without this flag.
2. Please use K = 2; TIMEOUT = 3* K  (recall these parameters pertain to timers related to Periodic operations of the switch and the Controller)
3. As mentioned earlier, all logs that you print must strictly follow the convention described.
4. Do not modify the provided configuration files.

## What you need to submit
The controller.py and switch.py codes. You are free to modify the sample config files as provided. 
**Do not submit any binaries. Your git repo should only contain source files; no products of compilation.**

## To submit:
 Create a tag named "submission" when you are ready to submit. You can use the following command or the github interface to do so.
> git tag -a submission -m "optional message"

This will show you if the tag is created:
> git tag

**Do not submit any binaries. Your git repo should only contain source files; no products of compilation.**

**Once you submit your grade will be given in "grade.txt" file in the branch 'grade'. It might take a few minutes for the branch to show up.**

## Grading
Grading will be based on the test configurations provided with the starter code and some hidden tests. Make sure you code is able to handle all failure and restart scenarios for full points.
