# Final Project - Map Reduce
![Architecture](./fig/Architecture.png "Architecture")
* **Deadline**: 12/09 (Friday)
* **Language**: C/C++
* **Implementation**: Serial, OpenMP, MPI, Hybrid

<br />

## Milestone
``` text
┌── [O]  Nov 07: Initialization
├── [O]  Nov 11: Project setup / Serial version
├── [O]  Nov 12: Deliver
├── [O]  Nov 18: (dev)
├── [O]  Nov 25: (dev)
├── [O]  Dec 02: Review / Report
└── [O]  Dec 09: Submission
```

## Directory Structure
``` python
project
├── doc
│   ├── Architecture.pdf
│   └── Slides.pdf
│
├── fig
│   ├── Algorithms.png
│   ├── Architecture.png
│   └── Folder.png
│
├── data
│   ├── renew
│   ├── files.zip -> ../main/files.zip
│   ├── 1.txt       # ──┐
│   ├── (...)       # ──┤ Input files
│   └── 16.txt      # ──┘
│
├── serial          # Codebase Structure -------------------\
│   ├── data -> ../data                                 #   |
│   ├── bin                                             #   |   (binary executable files)
│   │   └── serial.o                                    #   |
│   │                                                   #   |
│   ├── src                                             #   |   (algorithms part)
│   │   ├── algo.cpp                                    #   |   CORE cpp files
│   │   ├── serial.cpp                                  #   |
│   │   ├── openmp.cpp                                  #   |
│   │   ├── mpi.cpp                                     #   |
│   │   └── utility.cpp                                 #   |
│   │                                                   #   |
│   ├── include                                         #   |   (header files)
│   │   ├── algo.hpp                                    #   |
│   │   └── utility.hpp                                 #   |
│   │                                                   #   |
│   ├── makefile                                        #   |   compile, run
│   ├── main.cpp                                        #   |
│   │                                                   #   |
│   ├── serial.o -> ./bin/serial.o                      #   |
│   │                                                   #   |
│   ├── README.md                                       #   |
│   ├── result.log                                      #   |   wordCount results
│   └── files.zip # ------------------------------------#   |   archived input files

├── user-Mike       # OpenMP / MPI
│
└── README.md
```

## Algorithms
![Algorithms](./fig/Algorithms.png "Algorithms")