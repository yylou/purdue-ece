/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (Data Structures and Algorithms)
*/

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
std::map<int,int> readersClockOut;                      // for mapper to stop pushing work items to reducer queues
int mappersClockOut = 0;                                // for reducer to stop getting work items from reducer queues
std::map<std::string,int> hashTable;                    // [FINAL ANSWER]

omp_lock_t queueContentLocks[numFiles];
omp_lock_t queueDataLocks[numFiles];
omp_lock_t readerLock, mapperLock, counterLock;

void init(int maxThreads) {
    threads = maxThreads;
    
    int filesPerThread = numFiles / threads;            // ──┐ divmod 
    int remain = numFiles - filesPerThread * threads;   // ──┘ 

    /*  (1) Queue Container: each element is a queue for a specific thread  */
    int prev = 1;
    for (int tid=0 ; tid<threads ; ++tid) {
        contentQueueContainer.emplace_back(std::queue<WorkItem>());
        dataQueueContainer.emplace_back(std::queue<WorkItem>());

        /*  (2) Files Map: each thread is assigned with 0+ files  */
        int fid;
        for (fid=prev ; fid<(prev + filesPerThread + (tid < remain)) ; ++fid) {
            filesMap[tid].push_back("./data/" + std::to_string((int) fid) + ".txt");
        }
        prev = fid;
    }

    /*  (3) Lock initialization  */
    for(int i=0 ; i<numFiles ; i++) {
        omp_init_lock(&queueContentLocks[i]);
        omp_init_lock(&queueDataLocks[i]);
    }
    omp_init_lock(&readerLock);
    omp_init_lock(&mapperLock);
    omp_init_lock(&counterLock);
}

int getFilesMapSize    (int queueId) { return filesMap[queueId].size(); }
int getMapperQueueSize (int queueId) { return contentQueueContainer[queueId].size(); }
int getReducerQueueSize(int queueId) { return dataQueueContainer[queueId].size();    }

void wrapWorkItems(int queueId, std::string line) {
    std::string word;
 
    for (std::istringstream is(line) ; is>>word ; ) {
        if (word == " " || line.empty()) continue;
        WorkItem workItem(word, 1);

        omp_set_lock(&queueContentLocks[queueId]);
        contentQueueContainer[queueId].push(workItem);
        omp_unset_lock(&queueContentLocks[queueId]);
    }
}

void putMapper(int queueId) {
    if (filesMap[queueId].size() == 0) return;

    for (const auto& fileName : filesMap[queueId]) {
        std::ifstream inputFile(fileName);

        if (inputFile.is_open()) {
            // #ifdef LOG
            log("Parse", fileName+"\n", 0);
            // #endif

            std::string line;
            while (getline(inputFile, line)) {      // line by line
                wrapWorkItems(queueId, line);       // word by word -> put work items to queue by id
            }
            line.clear();

        } else {
            log("FILE NOT FOUND", fileName+"\n", 0);
        }

        omp_set_lock(&readerLock);
        ++readersClockOut[queueId];                  // reader clocks in when finishing
        inputFile.close();
        omp_unset_lock(&readerLock);
    }
}

void putReducer(int queueId, int size) {
    std::hash<std::string> hash;
    std::vector<WorkItem> workItems;
    std::map<std::string,int> counter;
    
    while (readersClockOut[queueId] < filesMap[queueId].size() ||
           getMapperQueueSize(queueId) > 0) {       // TRUE @ reader is reading OR queue is not empty

        #ifdef LOG
        log("Retrieve", std::to_string(queueId)+"\n", 0);
        #endif

        /*  (1) GET work items  */
        omp_set_lock(&queueContentLocks[queueId]);
        while (getMapperQueueSize(queueId) > 0 && workItems.size() < size) {
            workItems.push_back(contentQueueContainer[queueId].front());
            contentQueueContainer[queueId].pop();
        }
        omp_unset_lock(&queueContentLocks[queueId]);

        #ifdef LOG
        log("Combine", std::to_string(queueId)+"\n", 0);
        #endif

        /*  (2) COMBINE records (work items)  */
        for (const auto& iter : workItems) {
            ++counter[iter.word];
        }

        #ifdef LOG
        log("Push (mapper -> reducer)", std::to_string(queueId)+"\n", 0);
        #endif
        
        /*  (3) PUSH to reducer queue by hash functions  */
        for (const auto& [word, count] : counter) {
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", word.c_str(), count, hash(word));
            tmpCounter += count;
            #endif
            
            WorkItem workItem(word, count);
            int reducerQueueId = hash(word) % threads;  // hash to get recuder queue id
            
            omp_set_lock(&queueDataLocks[reducerQueueId]);
            dataQueueContainer[reducerQueueId].push(workItem);
            omp_unset_lock(&queueDataLocks[reducerQueueId]);
        }

        workItems.clear();
        counter.clear();
    }

    // omp_set_lock(&mapperLock);
    mappersClockOut++;   // mapper clocks in when finishing
    // omp_unset_lock(&mapperLock);
}

void getReducer(int queueId, int size) {
    std::vector<WorkItem> workItems;

    while (mappersClockOut != 1 ||
           getReducerQueueSize(queueId) > 0) {      // TRUE @ mapper is combining OR queue is not empty
        
        omp_set_lock(&queueDataLocks[queueId]);
        while (getReducerQueueSize(queueId) > 0 && workItems.size() < size) {
            workItems.push_back(dataQueueContainer[queueId].front());
            dataQueueContainer[queueId].pop();
        }
        omp_unset_lock(&queueDataLocks[queueId]);

        #ifdef LOG
        log("Count", "\n", 0);
        #endif

        omp_set_lock(&counterLock);
        for (const auto& iter : workItems) { hashTable[iter.word] += iter.count; }
        omp_unset_lock(&counterLock);

        workItems.clear();
    }
}

void printWordCount() {
    for (const auto& pair : hashTable) {
        printf("%50s  |  %10d\n", pair.first.c_str(), pair.second);
    }
}
