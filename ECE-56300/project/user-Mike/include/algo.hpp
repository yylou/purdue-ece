/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (algorithm header file)
*/

#include <queue>
#include <vector>
//#include <mpi.h>

typedef struct WorkItem {
    std::string word;
    int count;

    WorkItem(std::string word_, int count_) {
        word  = word_;
        count = count_;
    }
} WorkItem;

typedef std::queue<WorkItem> Queue;
typedef std::vector<Queue> QueueContainer;

void init(int maxThreads);
int getMapperQueueSize(int queueID);
int getReducerQueueSize(int queueID);
void wrapWorkItems(int queueId, std::string line);
void putMapper(int queueId);
void putReducer1(int queueId, int size);
void getReducer(int queueId, int size);
void printWordCount();

//void algo_Serial(int maxThreads);
void algo_OpenMP(int maxThreads);
//void algo_MPI(int maxThreads, int &numP, int &rank, MPI_Status &status);