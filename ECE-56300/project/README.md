# Final Project - Map Reduce
![Architecture](./fig/Architecture.png "Architecture")
* **Deadline**: 12/09 (Friday)
* **Language**: C/C++
* **Implementation**: Serial, OpenMP, MPI, Hybrid

<br />

## Timeline
``` text
┌── Nov 07: Initialization
├── Nov 11: 
├── Nov 18: 
├── Nov 25: 
├── Dec 02: 
└── Dec 09: 
```

## Directory Structure
``` python
project
├── doc
│   └── Architecture.pdf
│
├── fig
│   └── Architecture.png
│
├── data
│   ├── renew       # Cmd to unzip input files
│   ├── files.zip   # Symbolic link to zipped archive file
│   ├── 1.txt       # ──┐
│   ├── (...)       # ──┤ Input files
│   └── 16.txt      # ──┘
│
├── main            # Codebase <------------------------\
│   └──             #                                   |
│                                                     # |
│                                                     # | (through rsync)
│                                                     # | 
├── user-Arnold     # OpenMP or MPI                     |
├── user-Jeff       # OpenMP or MPI                     |
├── user-Mike       # Skeleton code / Report <----------/
│
└── README.md
```

## Setup
``` shell
1. 
2. 
3. 
4. 
5. 
```

## Evaluation
``` text
[TIMING]
1. 
2. 
3. 
4. 
5. 

[SPEEDUP (#FILES=16)]
1. Serial
2. OpenMP: 1, 2, 4, 8, 16 (threads)
3. MPI: 1, 2, 4, 8, 16 (nodes) with 16 threads (each core)
4. Hybrid: (same as MPI)

[PERFORMANCE]
1. Karp-Flatt Analysis
```