/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (OpenMP version)
*/

#include <omp.h>

#include <utility.hpp>
#include <algo.hpp>

#define LOG

void algo_OpenMP(int maxThreads, int size) {
    const int threads = maxThreads;
    omp_set_num_threads(maxThreads);

    double time_init, time_mapReduce;

    #ifdef LOG
    log("[   Init  ]    |    Queue & Lock  (#threads", std::to_string(threads)+")\n", 0);
    #endif
    /*  [STEP 0]
        1. INIT queues and thread-locks
        2. ASSIGN files to each thread or process
    */
    time_init = -omp_get_wtime();
    init(threads);
    time_init += omp_get_wtime();

    time_mapReduce = -omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp master
        {
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
                #pragma omp task
                putMapper(tid);
            }

            // #pragma omp taskwait

            #ifdef LOG
            log("[ Combine ]    |    Put", "mapper -> reducer\n", 0);
            #endif
            /*  [STEP 2]
                (for each thread)
                1. COMBINE records by SIZE=20
                2. PUSH to reducer queue by hash function
            */
            for (int tid=0 ; tid<threads ; tid++) {
                #pragma omp task
                putReducer(tid, size);    // aka. getMapper(...)
            }

            // #pragma omp taskwait

            #ifdef LOG
            log("[  Count  ]    |    Get", "reducer\n", 0);
            #endif
            /*  [STEP 3]
                (for each thread)
                1. GET combined records by SIZE=20
                2. COUNT words
            */
            for (int tid=0 ; tid<threads ; tid++) {
                #pragma omp task
                getReducer(tid, size);
            }

            #pragma omp taskwait
        }
    }
    time_mapReduce += omp_get_wtime();

    printWordCount();

    log("Init (OpenMP)      ", std::to_string(time_init)+"\n", 0);
    log("MapReduce (OpenMP) ", std::to_string(time_mapReduce)+"\n", 0);
}