# Running the example code (and your implementatations) locally
1. Choose a configuration for the run. Test configurations are available in the TestConfig directory. Say we choose: config1.ini
2. Run the emulator in the Emulator directory.
   python3 emulator.py ../TestConfig/config1.ini
3. Run the receiver in the example (or your implementation directory) directory in the Student Code directory.
   
   make run-receiver config=../../TestConfig/config1.ini
   
   OR
   
   python3 receiver.py ../../TestConfig/config1.ini
   
4. Run the sender in the example (or your implementation directory) directory in the Student Code directory.
   
   make run-sender config=../../TestConfig/config1.ini
   
   OR
   
   python3 sender.py ../../TestConfig/config1.ini
   
   Note:
   * Be careful to use the same configuration for emulator, sender and receiver.
   * Be careful about the path for the configuration.
   * The outputs for sender and receiver will be logged in sender_monitor.log and receiver_monitor.log respectively.
  
         * sender_monitor.log will describe the performance metrics: overhead and goodput.
  
         * recevier_monitor.log will describe whether was transmitted correctly.
   
   More details are available in the handout.
