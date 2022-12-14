/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (Serial version)
*/

#include <mpi.h>
//#include <omp.h>
#include <utility.hpp>
#include <algoMpi.hpp>

#define LOG


//int &numP, int &rank, MPI_Status &status, MPI_Datatype &Particletype
void algo_MPI(int maxThreads, int &numP, int &rank, MPI_Status &status, MPI_Datatype &Particletype) {
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

    if((numP/3 > rank) && (rank >= 0)){
	//init(threads);
        putMapper(rank, Particletype);
    }
    //MPI_Barrier(MPI_COMM_WORLD);

    // if(rank == 0){
    //     MPI_Bcast(&contentQueueContainer, contentQueueContainer.size(), MPI_BYTE, 0, MPI_COMM_WORLD);
    // }

    
    #ifdef LOG
    log("[ Combine ]    |    Put", "mapper -> reducer\n", 0);
    #endif

        /*  [STEP 2]
            (for each thread)
            1. COMBINE records by SIZE=20
            2. PUSH to reducer queue by hash function
        */
        // aka. getMapper(...)
    if((2 * numP / 3 > rank) && (rank >= numP / 3)){
        //init2(threads); 
        printf("rank %d entering putreducer\n", rank);
        putReducer(rank%3, 20, status, Particletype);
    }
    //MPI_Barrier(MPI_COMM_WORLD);




    #ifdef LOG
    log("[  Count  ]    |    Get", "reducer\n", 0);
    #endif
        /*  [STEP 3]
            (for each thread)
            1. GET combined records by SIZE=20
            2. COUNT words
        */
    if((numP > rank) && (rank >= 2 * numP / 3)){
        //init2(threads);
        getReducer(rank%3, 20, status, Particletype);
    }

    printWordCount();
}
