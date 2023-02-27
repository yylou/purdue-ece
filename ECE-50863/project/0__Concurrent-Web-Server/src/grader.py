#! /usr/bin/python
import sys, subprocess
import time
import socket

SERVER = "server.py"
CLIENT = "client.py"

FILE = "testfile.txt"
STUDENT = "student_output"
OUTPUT = "output-tmp.txt"

comments = ""


def check_output(idx):
    """Checks a single client (idx) output against the test file
    Also checks for the time delay between sent and received message.
    Args:
        idx (int): Index of the client being tested
    Returns:
        tuple (comment, grade): A grade of 5 is returned for correct
                                A grade of 2.5 is returned for bad timing
    """
    comment = ""
    datalines = ""
    grade = 5
    try:
        fout = open(STUDENT + str(idx))
        datalines = fout.readlines()

        # Find timestamps in file
        send_timestamp_line, recv_timestamp_line = -1, -1
        for i in range(len(datalines)):
            if "sent to the server" in datalines[i].lower():
                send_timestamp_line = i
            if "received from the server" in datalines[i].lower():
                recv_timestamp_line = i

        if send_timestamp_line == -1:
            comment = comment + "\nCould not find send timestamp. Line with \"<timestamp> Sent to the Server : \" not found."
            return comment, 0
        if recv_timestamp_line == -1:
            comment = comment + "\nCould not find received from server timestamp. Line with \"<timestamp> Received from the server : \" not found."
            return comment, 0

        sent_line = datalines[send_timestamp_line].split(" ")
        sent_timestamp = float(sent_line[0])

        recv_line = datalines[recv_timestamp_line].split(" ")
        recv_timestamp = float(recv_line[0])

        # Allow for 5 second buffer (10 seconds expected database delay)
        if (recv_timestamp - sent_timestamp) < 10:
            comment = comment + "\nDatabase delay missing. Add the simulated delay of 10 seconds."
            grade = grade - 2.5
        elif (recv_timestamp - sent_timestamp) > 15:
            comment = comment + "\nYour server did not respond within time. Concurrent execution failed."
            grade = grade - 2.5

        readfile = ''.join(datalines[recv_timestamp_line + 1: len(datalines) - 1])
        fout.close()
    except Exception as e:
        comment = comment + "\nError: " + str(e)
        comment = comment + "\nError while reading student output. \n " + str(
            "\n".join([str(elem) for elem in datalines]))
        return comment, 0

    file = open(FILE)
    filelines = ''.join(file.readlines())

    if filelines.strip() == readfile.strip():
        comment = comment + "\nCorrectly received file for client " + str(idx)
    else:
        comment = comment + "\nReceived file is not the same"
        grade = grade - 5

    file.close()
    return comment, grade


def clean_files():
    """This function is to remove any file created through grading. And students code,and object file.
    """
    proc = subprocess.Popen(['rm', STUDENT + "1", STUDENT + "2"], stdout=None, stderr=None)
    out, err = proc.communicate()


def find_open_port(startport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        startport += 1
        try:
            sock.bind(('', startport))
        except:
            continue
        break
    sock.close()
    return startport


def main():
    """Main code for launching as testing student submissions for Lab Exercise 1
    """
    global comments
    final_grade = 0
    err = ""

    comments = comments + "\nTesting concurrent web server with 2 clients requesting at the same time.\n"
    # Student output is piped to these files
    fout1 = open(STUDENT + "1", 'w+')
    fout2 = open(STUDENT + "2", 'w+')

    server_port = find_open_port(8001)
    print(f'Server port is {server_port}')
    client_1_port = find_open_port(server_port)
    client_2_port = find_open_port(client_1_port)

    # Launch the server
    server_proc = subprocess.Popen(['python', SERVER, str(server_port)], stdout=subprocess.PIPE, stderr=None)
    print("Launched Server: ", server_proc.pid, server_port)

    # Launch the Clients
    command = "python -O " + CLIENT + " localhost " + str(server_port) + " " + str(client_1_port)
    client_proc1 = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=fout1, stderr=subprocess.STDOUT)
    print("Launched Client: ", client_proc1.pid, client_1_port)

    command = "python -O " + CLIENT + " localhost " + str(server_port) + " " + str(client_2_port)
    client_proc2 = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=fout2, stderr=subprocess.STDOUT)
    print("Launched Client: ", client_proc2.pid, client_2_port)

    testout, err1 = client_proc1.communicate()
    testout, err2 = client_proc2.communicate()

    # Give it a sec
    time.sleep(1)

    # Kill the processes
    print("Killing Processes")
    server_proc.kill()
    client_proc1.kill()
    client_proc2.kill()

    fout1.close()
    fout2.close()

    if err1:
        print("Got error in Client " + str(client_proc1.pid) + " : " + err1)
        comments = comments + "\nGot error in Client " + str(client_proc1.pid) + " : " + err1
    else:
        comments = comments + "\n\nChecking response for Client 1 :"
        comment, grade = check_output(1)
        comments = comments + comment
        final_grade = final_grade + grade

    if err2:
        print("Got error in Client " + str(client_proc2.pid) + " : " + err2)
    else:
        comments = comments + "\n\nChecking response for Client 2 :"
        comment, grade = check_output(2)
        comments = comments + comment
        final_grade = final_grade + grade

    # Write the grade and comments to file
    student = open(OUTPUT, 'w+')
    student.write("Total Grade " + str(final_grade) + " out of 10\n\n")
    student.write("Output: " + comments)
    student.close()

    # Write number grade to file
    with open("grade-tmp.txt", 'w+') as f:
        f.write(str(final_grade))


# clean_files()

if __name__ == "__main__":
    main()