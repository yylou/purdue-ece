/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (Serial version)
*/

//#include <mpi.h>
#include <omp.h>

#include <utility.hpp>
#include <algo.hpp>

#define LOG

void algo_Serial(int maxThreads) {
    const int threads = maxThreads;

    #ifdef LOG
    log("[   Init  ]    |    Queue & Lock  (#threads", std::to_string(threads)+")\n", 0);
    #endif
    /*  [STEP 0]
        1. INIT queues and thread-locks
        2. ASSIGN files to each thread or process
    */
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
    for (int tid=0 ; tid<threads ; tid++) {
        putMapper(tid);
    }

    #ifdef LOG
    log("[ Combine ]    |    Put", "mapper -> reducer\n", 0);
    #endif
    for (int tid=0 ; tid<threads ; tid++) {
        /*  [STEP 2]
            (for each thread)
            1. COMBINE records by SIZE=20
            2. PUSH to reducer queue by hash function
        */
        putReducer(tid, 20);    // aka. getMapper(...)

    }

    #ifdef LOG
    log("[  Count  ]    |    Get", "reducer\n", 0);
    #endif
    for (int tid=0 ; tid<threads ; tid++) {
        /*  [STEP 3]
            (for each thread)
            1. GET combined records by SIZE=20
            2. COUNT words
        */
        getReducer(tid, 20);
    }

    printWordCount();
}