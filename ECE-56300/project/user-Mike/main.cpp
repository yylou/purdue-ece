/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/06

Project : Purdue ECE56300 - Project
Version : v1.0
*/

#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <utility.hpp>
#include <algo.hpp>

int main (int argc, char *argv[]) {
    
    
    const int maxThreads = atoi(argv[1]);
    char* type = argv[2];
    char* mode = argv[3];
    const std::string serial = "serial";
    const std::string parall = "parall";
    const std::string opnemp = "omp";
    const std::string mpi    = "mpi";


    /* =========================================================================== *\
    |    Serial (simulate parallel version)
    \* =========================================================================== */
    if (compareString(type, serial.c_str())) {
        
        log("Running serial version", "src/serial.cpp\n", 1);
        algo_Serial(maxThreads);
        log("Done", "(Serial version)\n", 0);


    /* =========================================================================== *\
    |    Parallel
    \* =========================================================================== */
    } else if (compareString(type, parall.c_str())) {

        /* ----------------------------------------------------------------------- *\
        |*      OpenMP -> FIND "algo.cpp" TO IMPLEMENT
        \* ----------------------------------------------------------------------- */
        if (compareString(mode, opnemp.c_str())) { 
            
            log("Running parallel version: OPENMP", "src/openmp.cpp\n", 1);

            algo_OpenMP(maxThreads);


        /* ----------------------------------------------------------------------- *\
        |*      MPI    -> FIND "algo.cpp" TO IMPLEMENT
        \* ----------------------------------------------------------------------- */
        } else if (compareString(mode, mpi.c_str())) { 

            log("Running parallel version: MPI", "src/mpi.cpp\n", 1);
            algo_MPI();

        }
    }
}