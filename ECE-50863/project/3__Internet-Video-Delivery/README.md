# Adaptive Bit Rate (ABR)

This project is about implementing and evaluating Adaptive Bit Rate (ABR) algorithms for Internet video delivery. The project requires reading scientific papers, implementing and evaluating ABR algorithms on a custom simulator, and submitting a research report. The code structure includes a top-level simulator file, tester file, supporting code, and student files where algorithms need to be implemented. The project requires submitting two algorithms in separate files and running them using the command line. The grading criteria are based on implementing the required algorithms, presenting clear and well-thought-out results, and exhibiting creativity and effort in the open-ended components. Bonus marks may be awarded for particularly new and interesting algorithm variants and high effort and passion in the project.

## Usage
The simulator runs your algorithm and outputs statistics on a per-chunk basis as well as for the complete video as a whole. You can run the simulator with the following command:

```bash 
python simulator.py <path to the test file (.ini)> <Student algorithm to run> -v
```

The path to the test file should be the path to one of the .ini files in the tests/ directory. The student algorithm to run should be an integer 1 or 2 (or higher if you made more algorithms) to run student1.py or student2.py. ‘-v’ is an optional flag that enables verbose output for the simulation. This prints the download times and quality selections for each chunk.

For example, running:
```bash
python simulator.py tests/hi_avg_hi_var.ini 2 -v
```

will start the simulator running the test "hi_avg_hi_var.ini" using the algorithm in student2.py and enable verbose logging.

The tester will run your algorithm and output statistics for all test cases. It is called with
```bash
python tester.py <Student algorithm to run (1 or 2)>
```
