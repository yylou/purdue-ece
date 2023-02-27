# Example Directory

This is an example directory of how your protocol directory should look.

# Steps to be followed
In all cases, your code should follow the following steps in order to ensure proper functionality with the Network Emulator and Network Monitor.
1. Initialize the sender and receiver network monitors.
2. Start the receiver. After a short delay (~1 second), start the sender.
3. Exchange messages through Monitor.send() and Monitor.recv().
4. When the receiver receives the final packet in the message, call Monitor.recv_end(). IMPORTANT: Leave the receiver running and sending ACKs to any additional packets that may arrive!
5. When the sender receives an ACK for the final packet, call Monitor.send_end(). This will shut down the network emulator.

### Note: "to_send_small.txt" and "to_send_large.txt" are the files copied from ../files/. The choice of the file being transmitted can be set in the config files.