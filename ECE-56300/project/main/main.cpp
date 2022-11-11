/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/06

Project : Purdue ECE56300 - Project
Version : v1.0 (initialization)
*/

#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <omp.h>

int main (int argc, char *argv[]) {
    
    const char* mode = argv[1];
    const int maxThreads = atoi(argv[2]);

    printf("%s\n", mode);


}