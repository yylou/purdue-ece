/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (Data Structures and Algorithms)
*/

#include <mpi.h>
#include <omp.h>
#include <string>
#include <sstream>
#include <fstream>
#include <map>

#include <utility.hpp>
#include <algo.hpp>

// #define LOG
#define numFiles 15

std::map<int,std::vector<std::string>> filesMap;        // for reader threads to parse specified files
QueueContainer contentQueueContainer;                   // [MAPPER  QUEUE] for reader threads to put work items
QueueContainer dataQueueContainer;                      // [REDUCER QUEUE] for mapper threads to put combined record
int threads = 0;                                        // for mapper to put work items to reducer queues by hashing
std::map<int,int> readersClockIn;                       // for mapper to stop pushing work items to reducer queues
int mappersClockIn;                                     // for reducer to stop getting work items from reducer queues
std::map<std::string,int> hashTable;                    // [FINAL ANSWER]

void init(int maxThreads) {
    threads = maxThreads;
    
    int filesPerThread = numFiles / threads;
    int remain = numFiles - filesPerThread * threads;

    /* (1) Queue Container: each element is a queue for a specific thread  */
    int prev = 1;
    for (int tid=0 ; tid<maxThreads ; ++tid) {
        contentQueueContainer.emplace_back(std::queue<WorkItem>());
        dataQueueContainer.emplace_back(std::queue<WorkItem>());

        /*  (2) Files Map: each thread is assigned with 0+ files  */
        int fid;
        for (fid=prev ; fid<(prev + filesPerThread + (tid < remain)) ; ++fid) {
            filesMap[tid].push_back("./data/" + std::to_string((int) fid) + ".txt");
        }
        prev = fid;
    }

    /* (3) Lock initialization */




}

int getMapperQueueSize (int queueId) { return contentQueueContainer[queueId].size(); }
int getReducerQueueSize(int queueId) { return dataQueueContainer[queueId].size();    }

void wrapWorkItems(int queueId, std::string line) {
    #ifdef LOG
    log("[Line]", line+"\n", 0);
    #endif
    
    std::string word;    
    for (std::istringstream is(line) ; is>>word ; ) {
        if (word == " " || line.empty()) continue;
        WorkItem workItem(word, 1);

        /*  LOCK ACQUIRE  */
        contentQueueContainer[queueId].push(workItem);
        /*  LOCK RELEASE  */
    }
}

void putMapper(int queueId) {
    for (const auto& fileName : filesMap[queueId]) {
        std::ifstream inputFile(fileName);

        if (inputFile.is_open()) {
            #ifdef LOG
            log("Parse", fileName+"\n", 0);
            #endif

            std::string line;
            while (getline(inputFile, line)) {      // line by line
                wrapWorkItems(queueId, line);       // word by word -> put work items to queue by id
            }

        } else {
            log("FILE NOT FOUND", fileName+"\n", 0);
        }

        ++readersClockIn[queueId];                  // reader clocks in when finishing
    }
}

void putReducer(int queueId, int size) {
    int batch = size;
    std::hash<std::string> hash;
    std::vector<WorkItem> workItems;
    std::map<std::string,int> counter;
    if (getMapperQueueSize(queueId) == 0) return;

    while (readersClockIn[queueId] < filesMap[queueId].size() ||
           getMapperQueueSize(queueId) > 0) {       // TRUE @ reader is reading OR queue is not empty
        
        batch = size;
        while (getMapperQueueSize(queueId) > 0 && batch-- > 0) {
            workItems.push_back(contentQueueContainer[queueId].front());
            
            /*  LOCK ACQUIRE  */
            contentQueueContainer[queueId].pop();
            /*  LOCK RELEASE  */
        }

        #ifdef LOG
        log("Combine", "\n", 0);
        #endif

        for (const auto& iter : workItems) {
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", iter.word.c_str(), iter.count, hash(iter.word));
            #endif
            
            ++counter[iter.word];
        }

        #ifdef LOG
        log("Push (mapper -> reducer)", "\n", 0);
        int tmpCounter = 0;
        #endif
        
        for (const auto& [word, count] : counter) {
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", word.c_str(), count, hash(word));
            tmpCounter += count;
            #endif
            
            WorkItem workItem_(word, count);
            int reducerQueueId = hash(word) % threads;

            /*  LOCK ACQUIRE  */
            dataQueueContainer[reducerQueueId].push(workItem_);
            /*  LOCK RELEASE  */
        }

        #ifdef LOG
        printf("%50s  |  %10d  |\n", "(total)", tmpCounter);
        #endif

        workItems.clear();
        counter.clear();
    }

    mappersClockIn++;   // mapper clocks in when finishing
}

void getReducer(int queueId, int size) {
    int batch = size;
    std::vector<WorkItem> workItems;
    if (getReducerQueueSize(queueId) == 0) return;


    while (mappersClockIn < threads ||
           getReducerQueueSize(queueId) > 0) {      // TRUE @ mapper is combining OR queue is not empty
        
        batch = size;
        while (getReducerQueueSize(queueId) > 0 && batch-- > 0) {
            workItems.push_back(dataQueueContainer[queueId].front());
            
            /*  LOCK ACQUIRE  */
            dataQueueContainer[queueId].pop();
            /*  LOCK RELEASE  */
        }

        #ifdef LOG
        log("Count", "\n", 0);
        #endif

        for (const auto& iter : workItems) {
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", iter.word.c_str(), iter.count, hash(iter.word));
            #endif
            
            hashTable[iter.word]++;
        }

        workItems.clear();
    }
}

void printWordCount() {
    for (const auto& pair : hashTable) {
        printf("%50s  |  %10d\n", pair.first.c_str(), pair.second);
    }
}