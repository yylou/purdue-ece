# Project 2: Designing and Optimizing a Reliable Data Transmission Protocol

In this project, your goal is to design and implement a reliable transfer protocol that can achieve high goodput, and low overhead under diverse network conditions. You will compare your protocol with a baseline scheme for comparison, which you will also implement.  While we provide hints, the specific optimizations that you will implement in your protocol is up to you. While correctness of all implementations is a minimal requirement, the project will be primarily evaluated on (i) the kinds of optimizations you implement; (ii) the performance that you achieve; and (iii) a documentation of the performance of the schemes under different network conditions, along with a clear understanding of the design trade-offs. You will document the above information in a report, which is a mandatory requirement for the project.

## Running your code
------------
We will be testing your code using the configuration files similar to the ones provided under TestConfig in the starter code. The network emulator will be launched before the endpoints.

### Important
Do not modify the Emulator, Monitor or the provided test configurations. Such changes can lead to autograding errors.

## What you need to submit
------------
The directories corresponding to protocols implemented as mentioned in the Lab handout.
The report based on the provided template, and following all the guidelines.

## To submit:
----------
Create a tag named "submission" when you are ready to submit. You can use the following command or the github interface to do so.

``` bash
git tag -a submission -m "optional message"
```

This will show you if the tag is created:

```bash
git tag
```

Do not submit any binaries. Your git repo should only contain source files; no products of compilation.

Once you submit your grade will be given in "grade.txt" file in the branch 'grade'. It might take a few minutes for the branch to show up. 


## Grading
A minimal expectation for all protocol implementations is correctness. A major criterion for grading is your performance results, whether the overall trends make sense, and the effort and creativity you have shown in adding optimizations. The clarity of report (documenting the effort, appropriately presenting graphs and containing the right level of detail in the writing) will also be a factor.

**The grade reflected in grade.txt file is not your final grade. It is based on the correctness of the file transmission using your implemented protocols. If all test cases are able to transmit files 'reliably' then you get a score of 1. If there is any error in file transmission then you get a score of 0. The final grade is based on a combination of report and your implementation.**
