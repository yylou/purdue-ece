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
//#include <algo.hpp>
#include <algoMpi.hpp>
#include <mpi.h>

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
        //algo_Serial(maxThreads);
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
            //algo_OpenMP(maxThreads);


        /* ----------------------------------------------------------------------- *\
        |*      MPI    -> FIND "algo.cpp" TO IMPLEMENT
        \* ----------------------------------------------------------------------- */
        } else if (compareString(mode, mpi.c_str())) { 

            log("Running parallel version: MPI", "src/mpi.cpp\n", 1);
            int numP, rank;
            MPI_Init(&argc, &argv);
            MPI_Status status;
            MPI_Comm_size(MPI_COMM_WORLD, &numP);
            MPI_Comm_rank(MPI_COMM_WORLD, &rank);

            MPI_Datatype Particletype;
            const MPI_Datatype type[2] = {MPI_INT, MPI_BYTE};
            const int len_block[2] = {1, 1};
            const MPI_Aint offsets[2] = {0, 4};
            MPI_Type_create_struct(2, len_block, offsets, type, &Particletype);//creat MPI datatype
            MPI_Type_commit(&Particletype);

            algo_MPI(maxThreads, numP, rank, status, Particletype);
        }
    }
}