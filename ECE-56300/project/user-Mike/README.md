## System
![Architecture](./../fig/Architecture.png "Architecture")

## Directory Structure
![Folder](./../fig/Folder.png "Folder")
``` python
user-Mike
│
├── data -> ../data
├── bin
│   ├── serial.o
│   ├── openmp.o
│   └── mpi.o
│
├── src
│   ├── algo.cpp
│   ├── serial.cpp
│   ├── openmp.cpp
│   ├── mpi.cpp
│   └── utility.cpp
│
├── include
│   ├── algo.hpp
│   └── utility.hpp
│
├── makefile                        # compile, run
├── main.cpp
│
├── serial.o -> ./bin/serial.o
├── openmp.o -> ./bin/openmp.o
├── mpi.o    -> ./bin/mpi.o
│
├── README.md
├── REL                             # rsync to "main" folder
├── result.log                      # wordCount results
└── files.zip                       # input files
```

## Algorithms
![Algorithms](./../fig/Algorithms.png "Algorithms")
