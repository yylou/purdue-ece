/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (utility header file)
*/

#include <cstdlib>
#include <iostream>
#include <cstring>

<<<<<<< HEAD:ECE-56300/project/user-Jeff/include/utility.hpp
int compareString(char* src, const char* target);
void log(std::string message, std::string argu, int skip);
=======
#include <utility.hpp>
#include <algo.hpp>

#define LOG

void algo_MPI(int numProc, int pid, int size) {
    const int threads = numProc;
    double time_init, time_mapReduce;

    #ifdef LOG
    log("[   Init   ]    |    Queue & Lock  (#threads", std::to_string(threads)+")\n", 0);
    #endif
    /*  [STEP 0]
        1. INIT queues and thread-locks
        2. ASSIGN files to each thread or process
    */
    time_init = -omp_get_wtime();
    init(threads);

    #ifdef LOG
    log("[  Parse  ]    |    Put", "reader -> mapper\n", 0);
    #endif
    /*  [STEP 1]
        (for each thread)
        1. READ files 
        2. PARSE line by line
        3. SPLIT line into words
        4. MAKE work item by each word
        5. PUSH to mapper queue by thread id
    */
    putMapper(pid);

    time_init     += omp_get_wtime();
    time_mapReduce = -omp_get_wtime();

    #ifdef LOG
    log("[ Combine ]    |    Put", "mapper -> reducer\n", 0);
    #endif
    /*  [STEP 2]
        (for each thread)
        1. COMBINE records by SIZE=20
        2. PUSH to reducer queue by hash function
    */
    putReducer(pid, size);    // aka. getMapper(...)

    #ifdef LOG
    log("[  Count  ]    |    Get", "reducer\n", 0);
    #endif
    for (int tid=0 ; tid<threads ; tid++) {
        /*  [STEP 3]
            (for each thread)
            1. GET combined records by SIZE=20
            2. COUNT words
        */
        getReducer(tid, size);
    }
    time_mapReduce += omp_get_wtime();

    printWordCount();

    log("Init (Serial)      ", std::to_string(time_init)+"\n", 0);
    log("MapReduce (Serial) ", std::to_string(time_mapReduce)+"\n", 0);
}
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023)):ECE-56300/project/user-Mike/src/mpi.cpp
