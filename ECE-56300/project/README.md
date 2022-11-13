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
├── [X]  Nov 18: (dev)
├── [X]  Nov 25: (dev)
├── [X]  Dec 02: Review / Report
└── [X]  Dec 09: Submission
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

## Algorithms
![Algorithms](./fig/Algorithms.png "Algorithms")

## Evaluation
``` text
[TIMING]
1. 
2. 
3. 
4. 
5. 

[SPEEDUP (#FILES=15)]
1. Serial
2. OpenMP: 1, 2, 4, 8 (threads)
3. MPI: 1, 2, 4, 8 (nodes) with 3 threads (each core)
4. Hybrid: (OpenMP + MPI)

[PERFORMANCE]
1. Karp-Flatt Analysis
```