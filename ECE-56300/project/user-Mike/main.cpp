/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/06

Project : Purdue ECE56300 - Project
Version : v1.0
*/

#include <omp.h>
#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <utility.hpp>
#include <algo.hpp>
//#include <algoMpi.hpp>
//#include <mpi.h>

int main (int argc, char *argv[]) {
    
    const int param1 = atoi(argv[1]);
    const int param2 = atoi(argv[2]);
    char* type = argv[3];
    char* mode = argv[4];
    const std::string serial = "serial";
    const std::string parall = "parall";
    const std::string opnemp = "omp";
    const std::string mpi    = "mpi";

    double time;

    /* =========================================================================== *\
    |    Serial (simulate parallel version)
    \* =========================================================================== */
    if (compareString(type, serial.c_str())) {
        
        log("Running serial version", "src/serial.cpp\n", 1);
<<<<<<< HEAD
        //algo_Serial(maxThreads);
        log("Done", "(Serial version)\n", 0);
=======
        time = -omp_get_wtime();
        algo_Serial(param1, param2);
        time += omp_get_wtime();
        log("Done (Serial)      ", std::to_string(time)+"\n", 0);
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))


    /* =========================================================================== *\
    |    Parallel
    \* =========================================================================== */
    } else if (compareString(type, parall.c_str())) {

        /* ----------------------------------------------------------------------- *\
        |*      OpenMP -> FIND "algo.cpp" TO IMPLEMENT
        \* ----------------------------------------------------------------------- */
        if (compareString(mode, opnemp.c_str())) { 
            omp_set_num_threads(param1);
            
            log("Running parallel version: OPENMP", "src/openmp.cpp\n", 1);
<<<<<<< HEAD
            algo_OpenMP(maxThreads);
=======
            time = -omp_get_wtime();
            algo_OpenMP(param1, param2);
            time += omp_get_wtime();
            log("Done (OpenMP      )", std::to_string(time)+"\n", 0);
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))


        /* ----------------------------------------------------------------------- *\
        |*      MPI    -> FIND "algo.cpp" TO IMPLEMENT
        \* ----------------------------------------------------------------------- */
        } else if (compareString(mode, mpi.c_str())) {
            /*  initialization  */
            int pid, numProc, provided;
            MPI_Init(&argc, &argv);
            MPI_Comm_size(MPI_COMM_WORLD, &numProc);
            MPI_Comm_rank(MPI_COMM_WORLD, &pid);
            MPI_Barrier(MPI_COMM_WORLD);

            omp_set_num_threads(1);

            log("Running parallel version: MPI", "src/mpi.cpp\n", 1);
<<<<<<< HEAD
=======
            algo_MPI(numProc, pid, param2);

            MPI_Barrier(MPI_COMM_WORLD);
            MPI_Finalize();
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
        }
    }

    return 0;
}